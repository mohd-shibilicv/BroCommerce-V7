import json

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserBase
from App.models import Category, Product


class Command(BaseCommand):
    help = "Creates application data"

    def handle(self, *args, **kwargs):
        # Create Initial Categories
        json_data = """
        [
            {
                "stmt": "SELECT * FROM App_category;",
                "header": ["id", "name", "slug", "is_active"],
                "c_rows": [
                    ["3", "Motivational", "motivational", "1"],
                    ["4", "Fictional", "fictional", "1"],
                    ["5", "Drama", "drama", "1"],
                    ["6", "Non-Fiction", "non-fiction", "1"],
                    ["7", "New Releases", "new-releases", "1"],
                    ["8", "Sports", "sports", "1"]
                ]
            }
        ]
        """

        data = json.loads(json_data)
        rows = data[0]["c_rows"]
        for row in rows:
            category = Category(
                id=int(row[0]), name=row[1], slug=row[2], is_active=bool(int(row[3]))
            )
            category.save()

        # Create Initial Products
        product_data = """
            [
                {
                    "stmt": "SELECT * FROM App_product;",
                    "header": [
                        "id", "title", "author", "description", "image", "slug", "price",
                        "in_stock", "is_active", "created_at", "updated_at", "category_id",
                        "created_by_id", "stock_count"
                    ],
                    "p_rows": [
                        [
                            "4", "Atomic Habits", "admin",
                            "Atomic Habits",
                            "images/atomic_habits.jpg", "atomic-habits", "69.99", "1", "1",
                            "2023-10-17 04:27:10.320003", "2023-10-22 04:09:41.582615", "3", "1", "100"
                        ],
                        [
                            "5", "Spring", "admin",
                            "Spring",
                            "images/Spring.jpg", "spring", "84.45", "1", "1",
                            "2023-10-17 04:29:13.099721", "2023-10-22 04:09:27.674666", "4", "1", "100"
                        ],
                        [
                            "6", "The Merchant of Venice", "admin",
                            "The play is set in Venice and revolves around the
                            intertwined fates of several characters",
                            "images/The_Merchant_of_Venice.jpg", "the-merchant-of-venice", "87.33", "1", "1",
                            "2023-10-17 04:30:15.065996", "2023-10-22 04:01:57.483351", "5", "1", "100"
                        ],
                        [
                            "7", "The Mind of a Leader", "admin",
                            "The Mind of a Leader is a thought-provoking book",
                            "images/The_Mind_of_a_Leader.jpg", "the-mind-of-a-leader", "23.23", "1", "1",
                            "2023-10-17 04:30:59.295869", "2023-10-22 04:09:09.858386", "3", "1", "100"
                        ],
                        [
                            "8", "The Psychology of Money", "admin",
                            "The Psychology of Money is a captivating exploration of the 
                            complex relationship between individuals and their finances",
                            "images/The_Pyschology_of_Money.jpg", "the-psychology-of-money",
                            "98.44", "1", "1",
                            "2023-10-17 04:32:39.730399", "2023-10-22 04:08:48.672784",
                            "6", "1", "100"
                        ],
                        [
                            "9", "The Importance Of Being Earnest", "Oscar Wilde",
                            "Indulge in the delightful wit and satire of The Importance
                            of Being Earnest by Oscar Wilde",
                            "images/oscar_wilde.jpg", "the-importance-of-being-earnest", "29.99", "1", "1",
                            "2023-10-18 05:26:27.167120", "2023-10-22 04:00:13.640290", "5", "1", "100"
                        ],
                        [
                            "10", "Rich Dad Poor Dad: 25th Anniversary Edit: (25th Anniversary Edition)",
                            "Robert T. Kiyosaki",
                            "April of 2022 marks a 25-year milestone for the
                            personal finance classic Rich Dad Poor Dad",
                            "images/rich_dad_and_poor_dad.jpg",
                            "rich-dad-poor-dad-25th-anniversary-edit-25th-anniversary-edition",
                            "74.99", "1", "1",
                            "2023-10-18 05:28:39.453576", "2023-10-22 04:08:19.374882",
                            "6", "1", "100"
                        ],
                        [
                            "11", "Do It Today: Overcome procrastination, improve productivity and achieve more
                            meaningful things", "Darius Foroux",
                            "The International Bestseller DO IT TODAY",
                            "images/do_it_today.jpg",
                            "do-it-today-overcome-procrastination-improve-productivity-and-achieve-more-meaningful-things",
                            "33.43", "1", "1",
                            "2023-10-18 05:30:01.899273", "2023-10-22 04:07:59.425847",
                            "3", "1", "100"
                        ],
                        [
                            "12", "THINK AND GROW RICH", "Napoleon Hill",
                            "Since its publication",
                            "images/think_and_grow_rich.jpg", "think-and-grow-rich", "34.23", "1", "1",
                            "2023-10-18 05:32:55.164890", "2023-10-22 04:07:40.823875", "6", "1", "100"
                        ],
                        [
                            "13", "THE RICHEST MAN IN BABYLON", "George S. Clason",
                            "A mans wealth is not in the coins he carries in his purse",
                            "images/richest_man_in_babylone.jpg", "the-richest-man-in-babylon", "56.55", "1", "1",
                            "2023-10-18 05:35:20.757697", "2023-10-22 04:07:20.657569", "6", "1", "100"
                        ],
                        [
                            "14", "Ikigai", "Francesc Miralles",
                            "THE INTERNATIONAL BESTSELLER",
                            "images/ikigai.jpg", "ikigai", "90.1", "1", "1",
                            "2023-10-18 05:36:50.814289", "2023-10-22 04:07:02.158040", "6", "1", "100"
                        ],
                        [
                            "15", "THE CONCISE 48 LAWS OF POWER", "Robert Greene",
                            "The perfect gift book for the power hungry",
                            "images/48_laws_of_power.jpg", "the-concise-48-laws-of-power", "89.99", "1", "1",
                            "2023-10-18 05:38:38.960365", "2023-10-22 04:06:41.908341", "4", "1", "100"
                        ],
                        [
                            "16", "The Art of War (Deluxe Edition)", "Sun Tzu",
                            "This Collectable Hardbound Deluxe Edition",
                            "images/the_art_of_war.jpg", "the-art-of-war-deluxe-edition", "78.99", "1", "1",
                            "2023-10-18 05:40:05.414175", "2023-10-22 04:06:05.608593", "4", "1", "101"
                        ],
                        [
                            "17", "Madam Commissioner: The Extraordinary Life of an Indian Police Chief",
                            "Meeran Chadha Borwankar",
                            "The incredible memoir from one of Indias most uncompromising police officers",
                            "images/madam_commisionr.jpg",
                            "madam-commissioner-the-extraordinary-life-of-an-indian-police-chief",
                            "56.55", "1", "1",
                            "2023-10-18 05:42:14.691865", "2023-10-22 04:02:31.349327",
                            "7", "1", "0"
                        ],
                        [
                            "18", "Days at the Morisaki Bookshop : A charming and uplifting Japanese translated
                            story on the healing power of books", "Satoshi Yagisawa",
                            "A perfect blanket to warm every book lovers heart Reader review
                            I love Japanese literature",
                            "images/days_at.jpg",
                            "days-at-the-morisaki-
                            bookshop-a-charming-and-uplifting-japanese-translated-
                            story-on-the-healing-power-of-books",
                            "34.33", "1", "1",
                            "2023-10-18 05:44:24.932496", "2023-10-22 03:56:44.286320",
                            "5", "1", "100"
                        ],
                        [
                            "19", "MESSI (B PB): The must-read biography of the World Cup champion", "Guillem Balague",
                            "The story of one of the greatest footballers of all time",
                            "images/messi.jpg", "messi-b-pb-the-must-read-biography-of-the-world-cup-champion",
                            "23.33", "1", "1",
                            "2023-10-18 05:47:20.702596", "2023-10-22 03:55:25.472212",
                            "8", "1", "100"
                        ],
                        [
                            "20", "Cristiano Ronaldo: The Ultimate Fan Book", "Cristiano Ronaldo",
                            "Cristiano Ronaldo",
                            "images/ronaldo.jpg", "cristiano-ronaldo-the-ultimate-fan-book",
                            "25.66", "1", "1",
                            "2023-10-18 05:48:26.187167", "2023-10-22 03:47:33.485475",
                            "8", "1", "100"
                        ],
                        [
                            "21", "New Title", "the author", "The author description",
                            "images/default_user.png", "new-title", "99.99", "1", "1",
                            "2023-10-20 06:24:22.082971", "2023-10-22 04:10:21.371053",
                            "7", "1", "100"
                        ]
                    ]
                }
            ]
        """

        data = json.loads(product_data)
        rows = data[0]["p_rows"]

        for row in rows:
            product = Product(
                id=int(row[0]),
                title=row[1],
                author=row[2],
                description=row[3],
                image=row[4],
                slug=row[5],
                price=float(row[6]),
                in_stock=bool(int(row[7])),
                is_active=bool(int(row[8])),
                created_at=row[9],
                updated_at=row[10],
                category_id=int(row[11]),
                created_by_id=int(row[12]),
                stock_count=int(row[13]),
            )
            product.save()
