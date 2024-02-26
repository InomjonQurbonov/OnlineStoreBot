import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    # Work with categories
    def get_categories(self):
        categories = self.cursor.execute("SELECT id, category_name FROM categories;")
        return categories

    def get_products(self):
        products = self.cursor.execute("SELECT id, product_name FROM products;")
        return products

    def get_adds(self):
        ads = self.cursor.execute("SELECT id, ad_title FROM ads;")
        return ads

    def add_category(self, new_cat):
        categories = self.cursor.execute(
            "SELECT id, category_name FROM categories WHERE category_name=?;",
            (new_cat,)).fetchone()
        print(categories)
        if not categories:
            try:
                self.cursor.execute(
                    "INSERT INTO categories (category_name) VALUES(?);",
                    (new_cat,)
                )
                self.conn.commit()
                res = {
                    'status': True,
                    'desc': 'Successfully added'
                }
                return res
            except Exception as e:
                res = {
                    'status': False,
                    'desc': 'Something error, please, try again'
                }
                return res
        else:
            res = {
                'status': False,
                'desc': 'exists'
            }
            return res

    def upd_category(self, new_cat, old_cat):
        categories = self.cursor.execute(
            "SELECT id, category_name FROM categories WHERE category_name=?;",
            (new_cat,)
        ).fetchone()

        if not categories:
            try:
                self.cursor.execute(
                    "UPDATE categories SET category_name=? WHERE category_name=?;",
                    (new_cat, old_cat)
                )
                self.conn.commit()
                res = {
                    'status': True,
                    'desc': 'Successfully updated'
                }
                return res
            except Exception as e:
                res = {
                    'status': False,
                    'desc': 'Something error, please, try again'
                }
                return res
        else:
            res = {
                'status': False,
                'desc': 'exists'
            }
            return res

    def edit_category(self, new_name, id):
        try:
            self.cursor.execute(
                "UPDATE categories SET category_name=? WHERE id=?",
                (new_name, id)
            )
            self.conn.commit()
            return True
        except:
            return False

    def delete_category(self, cat_name):
        try:
            self.cursor.execute(
                "DELETE FROM categories WHERE category_name=?",
                (cat_name,)
            )
            self.conn.commit()
            res = {
                'status': True,
                'desc': 'Successfully deleted'
            }
        except Exception as e:
            res = {
                'status': False,
                'desc': 'Something error, please, try again'
            }
        return res

    def add_product(self, product_name, product_image, product_category):
        try:
            self.cursor.execute(
                "INSERT INTO products (product_name, product_image, product_category) VALUES(?, ?, ?);",
                (product_name, product_image, product_category)
            )
            self.conn.commit()
            res = {
                'status': True,
                'desc': 'Successfully added'
            }
        except Exception as e:
            res = {
                'status': False,
                'desc': 'Something error, please, try again'
            }
        return res

    def edit_product(self, id, new_product_name=None, new_product_image=None, new_product_category=None):
        try:
            if new_product_name:
                self.cursor.execute(
                    "UPDATE products SET product_name=? WHERE id=?",
                    (new_product_name, id)
                )
            if new_product_image:
                self.cursor.execute(
                    "UPDATE products SET product_image=? WHERE id=?",
                    (new_product_image, id)
                )
            if new_product_category:
                self.cursor.execute(
                    "UPDATE products SET product_category=? WHERE id=?",
                    (new_product_category, id)
                )
            self.conn.commit()
            res = {
                'status': True,
                'desc': 'Successfully updated'
            }
        except Exception as e:
            res = {
                'status': False,
                'desc': 'Something error, please, try again'
            }
        return res

    def delete_products(self, product_name):
        try:
            self.cursor.execute(
                "DELETE FROM products WHERE product_name=?",
                (product_name,)
            )
            self.conn.commit()
            res = {
                'status': True,
                'desc': 'Successfully deleted'
            }
        except Exception as e:
            res = {
                'status': False,
                'desc': 'Something error, please, try again'
            }
        return res

    def insert_ad(self,u_id, title, text, price, image, phone, prod_id, date ):
        try:
            self.cursor.execute(
                f"INSERT INTO ads (ad_title, ad_text, ad_price, ad_images, ad_phone, ad_owner, ad_product, ad_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title, text, price, image, phone,u_id, prod_id, date)
            )
            self.conn.commit()
            return True
        except:
            return False

    def get_my_ads(self, u_id):
        ads = self.cursor.execute(
            f"SELECT id, ad_title, ad_text, ad_price, ad_images FROM ads WHERE ad_owner=?;",
            (u_id,)
        )
        return ads

    def edit_ad(self,upd_title, upd_text, upd_price, upd_image, upd_date,ad_title):
        try:
            ads = self.cursor.execute(
                "UPDATE ads SET ad_title=?, ad_text=?, ad_price=?, ad_images=?, ad_date=? WHERE ad_title=?;",
                (upd_title, upd_text, upd_price, upd_image, upd_date,ad_title)
            )
            self.conn.commit()
            return ads
        except:
            return False
    def delete_ad(self, ad_title):
        try:
            self.cursor.execute(
                "DELETE FROM ads WHERE ad_title=?",
                (ad_title,)
            )
            self.conn.commit()
            res = {
                'status': True,
                'desc': 'Successfully deleted'
            }
        except Exception as e:
            res = {
                'status': False,
                'desc': 'Something error, please, try again'
            }
        return res

    def search_ads(self, ad_title):
        try:
            ads = self.cursor.execute("SELECT ad_title,ad_text,ad_price,ad_image FROM ads WHERE ad_title LIKE ?;",(f"%{ad_title}%",))
            self.conn.commit()
            return ads
        except:
            return False

    def ads_list(self, ad_title):
        self.cursor.execute(
            "SELECT * FROM ads WHERE ad_title LIKE ?;",(f"%{ad_title}%",)
        )
        ads = self.cursor.fetchall()
        return ads



