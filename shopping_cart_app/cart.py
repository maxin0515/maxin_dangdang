# 自定义购物车项类
class CartItem():
    def __init__(self, book, amount):
        self.book = book
        self.amount = int(amount)

# 自定义购物车
class Cart():
    def __init__(self):
        self.book_list = []
        self.total = 0
        self.save = 0

    def total_price(self):
        ele = 0
        for i in self.book_list:
            ele += i.book.book_dprice*i.amount
        self.total = round(ele,2)
        return self

    def save_money(self):
        befor_save = 0
        for i in self.book_list:
            befor_save += i.book.book_price*i.amount
        self.save = round(befor_save - self.total,2)
        print("节省",self.save)
        return self
    # 定义添加购物车
    def add_books(self, book, amount):
        # 判断图书已经在购物车项列表中
        print("加入中")
        for i in self.book_list:
            if i.book == book:
                i.amount += int(amount)
                return self
        self.book_list.append(CartItem(book, int(amount)))
        print("加完了",self.book_list)
        return self

    def del_books(self, book):
        print("删除中")
        for i in self.book_list:
            if i.book == book:
                self.book_list.remove(i)
                print("删完了", self.book_list)
                return self