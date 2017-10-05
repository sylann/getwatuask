from psycopg2 import Error, connect

def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = connect("dbname='snapat' user='postgres' password='postgres'")
        print("Conn : ", conn)
        return conn
    except Error as e:
        print(e)

    return None

def login(umail):
    """ Requête permettant l'identification d'un utilisateur. On vient comparer le PW de la db avec
    celui qu'il a saisi.
    :param user_mail: mail saisi dans le formulaire.
    :return data: mot de passe associé au mail dans la db
    """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            print
            cur.execute("SELECT * FROM utilisateur WHERE umail = %s", (umail,))
        except Error as e:
            print("login_query : ", e)
            return None

        data = cur.fetchall()[0]
        user = {'user_id': data[0], 'lastname': data[1], 'firstname': data[2],
                 'mail': data[3], 'password': data[4]}

    print(user)
    return user

def get_user_by_id(user_id):
    """ Requête permettant l'identification d'un utilisateur. On vient comparer le PW de la db avec
    celui qu'il a saisi.
    :param user_mail: mail saisi dans le formulaire.
    :return data: mot de passe associé au mail dans la db
    """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            print
            cur.execute("SELECT * FROM utilisateur WHERE user_id = %s", (user_id,))
        except Error as e:
            print("login_query : ", e)
            return None

        data = cur.fetchall()[0]
        user = {'user_id': data[0], 'lastname': data[1], 'firstname': data[2],
                 'mail': data[3], 'password': data[4]}

    print(user)
    return user

def get_client_by_id(client_id):
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            print
            cur.execute("SELECT * FROM client WHERE client_id = %s", (client_id,))
        except Error as e:
            print("get_user_by_id : ", e)
            return None

        data = cur.fetchall()[0]
        client = {'client_id': data[0], 'name': data[1], 'address': data[2],
                 'cp': data[3], 'city': data[4], 'country': data[5],
                'phone': data[6], 'mail': data[7], 'id_user': data[8]}

    print(client)
    return client

def get_needs_from_client(client_id):
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT need_id FROM need "
                        "JOIN client ON (client.client_id = need.client_id) "
                        "WHERE need.client_id = %s "
                        "AND active = TRUE "
                        "ORDER BY need.status_id ASC, latest_date DESC", (client_id,))
        except Error as e:
            print("get_all_needs_query : ", e)

        data = cur.fetchall()[0]
        need = {'need_id': data[0]}

    print(need)
    return need

def get_needs_from_user(id_user):
    """ Requête permettant de récupérer tous les besoins d'un utilisateur sans filtre particuliers.
    Ils sont triés par OPEN et date au plus tard
    :return need_list: Liste de tous les needs actifs
    """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT c_name, title, latest_date, need.status_id, need_id FROM need "
                        "JOIN status ON (need.status_id = status.status_id) "
                        "JOIN client ON (client.client_id = need.client_id) "
                        "JOIN utilisateur ON (utilisateur.user_id = need.user_id) "
                        "WHERE need.user_id = %s "
                        "AND active = TRUE "
                        "ORDER BY need.status_id ASC, latest_date DESC", (id_user,))
        except Error as e:
            print("get_all_needs_query : ", e)

        needs = [{'client_name': row[0], 'title': row[1], 'latest_date': row[2],
                  'status_id': row[3], 'need_id': row[4]} for row in cur.fetchall()]
    print(needs)
    return needs

#TODO : Finish this query
def get_filter_needs(filter):
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM need "
                        "WHERE id_status IN (%s) "
                        "AND active_need = '0'", filter)
        except Error as e:
            print("get_filter_needs_query : ", e)
            needs_filtered = cur.fetchall()

    print(needs_filtered)
    return needs_filtered

def get_need_by_id(need_id):
    """ Select un besoin spécifique pour l'affiche
    :return need: need """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM need WHERE need_id = %s", (need_id,))
        except Error as e:
            print("select_need_query : ", e)

        data = cur.fetchall()[0]
        need = {'need_id': data[0], 'title': data[1], 'description': data[2],
                'creation_date': data[3], 'latest_date': data[4], 'month_duration': data[5],
                'day_duration': data[6], 'price_ht': data[7],
                'consultant_name': data[8], 'client_id': data[9],
                'status_id': data[10], 'active': data[11], 'user_id': data[12]}
    print(need)
    return need

def insert_need(title, description, creation_date, latest_date, month_duration,
                day_duration, price_ht, consultant_name, client_id, status_id, user_id):
    with create_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute("SELECT max(need_id) FROM need")
            max_id = [int(record[0]) for record in cur.fetchall()][0] + 1
            print("MAX : ", max_id)

            cur.execute("INSERT INTO need (need_id, title, description, creation_date, latest_date, "
                    "month_duration, day_duration, price_ht, consultant_name, client_id, "
                    "status_id, active, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s)",
                        (max_id, title, description, creation_date, latest_date, month_duration,
                        day_duration, price_ht, consultant_name, client_id, status_id, user_id))
        except Error as e:
            print("insert_need_query : ", e)

    return None

def update_need(title, description, creation_date, latest_date, month_duration,
                      day_duration, price_ht, consultant_name, client_id, status_id, user_id):
    with create_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute("UPDATE need SET title = %s, "
                        "description = %s ,"
                        "date = %s, "
                        "latest_date = %s,"
                        "month_duration = %s, "
                        "day_duration = %s, "
                        "price_ht = %s, "
                        "consultant_name = %s, "
                        "id_client = %s, "
                        "id_status = %s, "
                        "id_user = %s "
                        "WHERE id = %s",
                        (title, description, creation_date, latest_date, month_duration,
                      day_duration, price_ht, consultant_name, client_id, status_id, user_id, need_id))
        except Error as e:
            print("update_need : ", e)

    return None

def delete_need(need_id):
    """ Requête permettant de passer un need en inactif (= supprimer).
    :param id_need: id du need à rendre inactif
    """
    with create_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE need SET active = FALSE where id_need = %s", (need_id,))
        except Error as e:
            print("delete_need_query : ", e)

    return None

if __name__ == "__main__":
    pass
    login("valentinmele@gfi.com")
    #get_user_by_id(1)
    #get_client_by_id(1)
    #get_needs_from_client(1)
    #get_needs_from_user(1)
    #get_filter_needs()
    #get_need_by_id(2)
    #insert_need("TEST INSERT", "CECI EST UN TEST", "2017-10-21", "2017-11-02", 2, 1, 5157.25, "CONSULTANT NAME TESTI", 1, 1, 1)
    #update_need()
    #delete_need()



