class Book:
    """书籍类：封装书籍属性和状态管理"""
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title  # 书名
        self.author = author  # 作者
        self.isbn = isbn  # ISBN编号（唯一标识）
        self.available = True  # 是否可借，默认True

    def __str__(self):
        """返回书籍的可读字符串"""
        status = "可借" if self.available else "已借出"
        return f"书名：{self.title} | 作者：{self.author} | ISBN：{self.isbn} | 状态：{status}"

    def set_available(self, available: bool):
        """修改书籍可借状态"""
        self.available = available


class User:
    """用户类：封装用户属性和借阅操作"""
    def __init__(self, name: str, card_id: str):
        self.name = name  # 姓名
        self.card_id = card_id  # 借书卡号（唯一标识）
        self.borrowed_books = []  # 已借书籍列表

    def __str__(self):
        """返回用户的可读字符串"""
        borrowed_titles = [book.title for book in self.borrowed_books]
        borrowed_str = "、".join(borrowed_titles) if borrowed_titles else "无"
        return f"姓名：{self.name} | 借书卡号：{self.card_id} | 已借书籍：{borrowed_str}"

    def borrow_book(self, book: Book):
        """用户借书（内部方法，由Library调用）"""
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
            book.set_available(False)

    def return_book(self, book: Book):
        """用户还书（内部方法，由Library调用）"""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.set_available(True)


class Library:
    """图书馆管理类：统筹书籍、用户和借阅逻辑"""
    def __init__(self):
        self.books = {}  # 书籍字典：key=ISBN，value=Book对象
        self.users = {}  # 用户字典：key=借书卡号，value=User对象

    def add_book(self, book: Book):
        """添加书籍到图书馆"""
        if book.isbn in self.books:
            print(f"警告：ISBN {book.isbn} 的书籍《{book.title}》已存在，无需重复添加")
        else:
            self.books[book.isbn] = book
            print(f"书籍《{book.title}》（ISBN：{book.isbn}）已成功加入图书馆")

    def register_user(self, user: User):
        """注册用户到图书馆"""
        if user.card_id in self.users:
            print(f"警告：借书卡号 {user.card_id} 的用户《{user.name}》已注册，无需重复注册")
        else:
            self.users[user.card_id] = user
            print(f"用户《{user.name}》（借书卡号：{user.card_id}）已成功注册")

    def check_book_availability(self, isbn: str) -> bool:
        """检查指定ISBN的书籍是否可借"""
        if isbn not in self.books:
            print(f"错误：未找到ISBN为 {isbn} 的书籍")
            return False
        book = self.books[isbn]
        if book.available:
            print(f"书籍《{book.title}》（ISBN：{isbn}）当前可借")
            return True
        else:
            print(f"书籍《{book.title}》（ISBN：{isbn}）当前已借出，不可借")
            return False

    def borrow_book(self, card_id: str, isbn: str):
        """处理用户借书操作"""
        # 1. 检查用户是否存在
        if card_id not in self.users:
            print(f"错误：未找到借书卡号为 {card_id} 的用户，无法借书")
            return
        user = self.users[card_id]

        # 2. 检查书籍是否存在且可借
        if not self.check_book_availability(isbn):
            return
        book = self.books[isbn]

        # 3. 执行借书操作
        user.borrow_book(book)
        print(f"用户《{user.name}》成功借阅书籍《{book.title}》（ISBN：{isbn}）")

    def return_book(self, card_id: str, isbn: str):
        """处理用户还书操作"""
        # 1. 检查用户是否存在
        if card_id not in self.users:
            print(f"错误：未找到借书卡号为 {card_id} 的用户，无法还书")
            return
        user = self.users[card_id]

        # 2. 检查书籍是否存在
        if isbn not in self.books:
            print(f"错误：未找到ISBN为 {isbn} 的书籍，无法还书")
            return
        book = self.books[isbn]

        # 3. 检查用户是否借了该书
        if book not in user.borrowed_books:
            print(f"错误：用户《{user.name}》未借阅书籍《{book.title}》（ISBN：{isbn}），无法还书")
            return

        # 4. 执行还书操作
        user.return_book(book)
        print(f"用户《{user.name}》成功归还书籍《{book.title}》（ISBN：{isbn}）")

    def show_all_books(self):
        """展示图书馆所有书籍信息"""
        if not self.books:
            print("图书馆暂无书籍")
            return
        print("\n===== 图书馆书籍列表 =====")
        for book in self.books.values():
            print(book)
        print("==========================\n")

    def show_user_info(self, card_id: str):
        """展示指定用户的信息（含已借书籍）"""
        if card_id not in self.users:
            print(f"错误：未找到借书卡号为 {card_id} 的用户")
            return
        print("\n===== 用户信息 =====")
        print(self.users[card_id])
        print("====================\n")


# 测试示例
if __name__ == "__main__":
    # 1. 创建图书馆实例
    lib = Library()

    # 2. 添加书籍
    book1 = Book("Python编程：从入门到实践", "埃里克·马瑟斯", "9787115428028")
    book2 = Book("算法导论", "Thomas H. Cormen", "9787111407010")
    book3 = Book("数据结构与算法分析", "Mark Allen Weiss", "9787115546920")
    lib.add_book(book1)
    lib.add_book(book2)
    lib.add_book(book3)

    # 3. 注册用户
    user1 = User("张三", "U001")
    user2 = User("李四", "U002")
    lib.register_user(user1)
    lib.register_user(user2)

    # 4. 展示所有书籍
    lib.show_all_books()

    # 5. 检查书籍可借状态
    lib.check_book_availability("9787115428028")

    # 6. 用户借书
    lib.borrow_book("U001", "9787115428028")  # 张三借Python编程
    lib.show_user_info("U001")  # 查看张三的借阅信息
    lib.check_book_availability("9787115428028")  # 再次检查该书状态

    # 7. 尝试借阅已借出的书籍
    lib.borrow_book("U002", "9787115428028")  # 李四尝试借同一本书

    # 8. 用户还书
    lib.return_book("U001", "9787115428028")  # 张三归还Python编程
    lib.show_user_info("U001")  # 再次查看张三的信息
    lib.check_book_availability("9787115428028")  # 检查归还后的状态

    # 9. 尝试归还未借阅的书籍
    lib.return_book("U001", "9787111407010")  # 张三尝试归还未借的算法导论
