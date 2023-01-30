from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Pie:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.filling = db_data['filling']
        self.crust = db_data['crust']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator = None
        self.voters = []
        self.num_votes = db_data['num_votes']
    
    @staticmethod
    def validate_pie(pie):
        is_valid=True
        if len(pie['name'])<1:
            flash("Pie must have a name", "pie")
            is_valid=False
        if len(pie['filling'])<1:
            flash("Filling cannot be left blank", "pie")
            is_valid=False
        if len(pie['crust'])<1:
            flash("Crust cannot be left blank", "pie")
            is_valid=False
        return is_valid
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO pies (user_id, name, filling, crust) VALUES (%(user_id)s, %(name)s, %(filling)s, %(crust)s);"
        return connectToMySQL('pie_schema').query_db(query, data)

    @classmethod
    def get_all_pies_with_votes(cls):
        query = "SELECT pies.id, pies.user_id AS creator_id, name, COUNT(votes.pie_id) AS num_votes \
            FROM pies LEFT JOIN votes on votes.pie_id = pies.id GROUP BY pies.id ORDER BY num_votes DESC;"
        results = connectToMySQL('pie_schema').query_db(query)
        all_pies = []
        print(results)
        for row in results:
            pie_data = {'pie_id':row['id']}
            one_pie = cls(cls.get_one_pie(pie_data))
            creator_data={'id':row['creator_id']}
            creator = user.User.get_user_by_id(creator_data)
            one_pie.creator = creator
            one_pie.num_votes= row['num_votes']
            all_pies.append(one_pie)
        return all_pies

    @classmethod
    def get_pies_of_creator(cls, data):
        query = "SELECT * FROM pies LEFT JOIN users ON pies.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('pie_schema').query_db(query, data)
        creator_pies = []
        for row in results:
            one_pie = cls(row)
            creator_pies.append(one_pie)
        return creator_pies
    
    @classmethod
    def get_one_pie(cls, data):
        query = "SELECT * FROM pies WHERE id=%(pie_id)s;"
        result = connectToMySQL('pie_schema').query_db(query, data)
        print(result[0])
        return result[0]

    @classmethod
    def edit_pie(cls, data):
        query = "UPDATE pies SET name = %(name)s, filling= %(filling)s, crust= %(crust)s WHERE id = %(id)s;"
        return connectToMySQL('pie_schema').query_db(query, data)

    @classmethod
    def delete_pie(cls, data):
        query = "DELETE FROM pies WHERE id = %(id)s;"
        return connectToMySQL('pie_schema').query_db(query, data)

    @staticmethod
    def add_vote(data):
        query = "INSERT INTO votes (user_id, pie_id) VALUES (%(user_id)s, %(pie_id)s);"
        return connectToMySQL('pie_schema').query_db(query, data)

    @staticmethod
    def subtract_vote(data):
        query = "DELETE FROM votes WHERE user_id = %(user_id)s AND pie_id = %(pie_id)s"
        return connectToMySQL('pie_schema').query_db(query, data)



    # saving this just to go back and look at what I was thinking

    # @classmethod
    # def update_votes(cls, data):
    #     query1 = """SELECT * FROM pies 
    #         LEFT JOIN votes ON votes.pie_id = pies.id 
    #         LEFT JOIN users as voters ON votes.user_id = voters.id 
    #         WHERE pies.id = %(id)s;"""
    #     results = connectToMySQL('pie_schema').query_db(query1, data)
    #     pie = cls(results[0])
    #     for row in results:
    #         voter_info={
    #             'id': row['voters.id'],
    #             'first_name': row['first_name'],
    #             'last_name': row['last_name'],
    #             'email': row['email'],
    #             'password': row['password'],
    #             'created_at': row['users.created_at'],
    #             'updated_at': row['users.updated_at']
    #         }
    #         voter = user.User(voter_info)
    #         pie.voters.append(voter)
    #     vote_data={
    #         'id': pie.id,
    #         'num_votes': len(pie.voters)
    #     }
    #     query2 = "UPDATE pies SET num_votes = %(num_votes)s WHERE id = %(id)s;"
    #     return connectToMySQL('pie_schema').query_db(query2, vote_data)