from django.db import models

# Create your models here.
class Address(models.Model):
    address_id = models.IntegerField(primary_key=True)
    recipient_name = models.CharField(max_length=20)
    recipient_address = models.CharField(max_length=50)
    postcode = models.CharField(max_length=6)
    tel = models.CharField(max_length=20, null=True)
    addr_monil = models.CharField(max_length=20, null=True)
    addr_user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        db_table = 't_address'


class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=128)
    book_author = models.CharField(max_length=64)
    publishing_house = models.CharField(max_length=128)
    publication_time = models.DateField(null=True)
    revision = models.IntegerField(null=True)
    book_isbn = models.CharField(max_length=64, null=True)
    word_amount = models.CharField(max_length=64, null=True)
    page_amount = models.IntegerField(null=True)
    book_format = models.CharField(max_length=20, null=True)
    paper_size = models.CharField(max_length=64, null=True)
    book_wrapper = models.CharField(max_length=64, null=True)
    book_category = models.ForeignKey('Category', models.DO_NOTHING, db_column='book_category', blank=True, null=True)
    book_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    book_dprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    editor_recommend = models.TextField(null=True)
    content_introduce = models.TextField(null=True)
    author_introduce = models.TextField(null=True)
    book_catalog = models.TextField(null=True)
    media_review = models.TextField(null=True)
    excerpt_illustration = models.TextField(null=True)
    book_pic = models.TextField(null=True)
    series_name = models.CharField(max_length=128, null=True)
    printing_date = models.DateField(null=True)
    impression = models.CharField(max_length=64, null=True)
    inventory = models.IntegerField(null=True)
    shelves_date = models.DateField(null=True)
    customer_sgrade = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    book_status = models.IntegerField(null=True)
    sales = models.IntegerField(null=True)

    class Meta:
        db_table = 't_book'


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=20)
    books_amount = models.IntegerField(null=True)
    parent_id = models.IntegerField(null=True)

    class Meta:
        db_table = 't_category'


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    num = models.IntegerField(null=True)
    create_date = models.DateTimeField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_address = models.ForeignKey(Address, models.DO_NOTHING, null=True)
    order_user = models.ForeignKey('User', models.DO_NOTHING, null=True)
    status = models.IntegerField(null=True)

    class Meta:
        db_table = 't_order'


class OrderItems(models.Model):
    item_id = models.IntegerField(primary_key=True)
    item_book = models.ForeignKey('Book', models.DO_NOTHING, null=True)
    item_order = models.ForeignKey('Order', models.DO_NOTHING, null=True)
    item_book_amount = models.IntegerField(null=True)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 't_order_items'


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_mobile = models.CharField(max_length=30, null=True, db_column='user_email')
    user_password = models.CharField(max_length=40, null=True)
    user_name = models.CharField(max_length=20, null=True)
    user_status = models.IntegerField(null=True)
    user_solt = models.CharField(max_length=40)

    class Meta:
        db_table = 't_user'
