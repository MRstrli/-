import pymysql
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

# 进行对于数据库的链接，数据库地址为 127.0.0.1，用户名为 root ，密码为 laoli666 ，数据库名为 学生选课系统 ，端口号为 3307
host = "127.0.0.1"
user = "root"
password = "laoli666"
db = "学生选课系统"
port = 3307
conn = pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset="utf8")
cursor = conn.cursor()
def add_course(course_number,number,course_name,student_name,a,b):#实现选课功能
    #在t4选课信息表中插入数据，格式为：course_number,number,课程名称,学生名称,"3","成功"
    sql = "insert into t4选课信息表 values('%s','%s','%s','%s','%s','%s')" % (course_number,number,course_name,student_name,"3","成功")
    cursor.execute(sql)
    conn.commit()
#类似于add_course函数，实现退课功能
def delete_course(course_number,number):
    sql = "delete  from t4选课信息表 where 课程号='%s' and 学号='%s'" % (course_number, number)
    #执行如上的sql语句
    cursor.execute(sql)
    conn.commit()
#选课退课
def create_select_course_window1(number):
    select_course_window = tk.Toplevel()
    select_course_window.title("选课界面")
    select_course_window.geometry("400x400")
    # 创建“退课”按钮，调用delete_course函数
    def delete_course_func():
        course_number = var.get()
        delete_course(course_number, number)
    def add_course_func():
        course_number = var.get()
        # 在t7排课管理表中所对应的教师号
        sql = "select 教师号 from t7排课管理表 where 课程号='%s'" % (course_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        teacher_number = result[0][0]
        # 在t1课程信息表中查询对应课程编号的课程名称
        sql = "select 课程名称 from t1课程信息表 where 课程号='%s'" % (course_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        课程名称 = result[0][0]
        # 在对应t2学生信息表中查对应学号的学生名称
        sql = "select 学生姓名 from t2学生信息表 where 学号='%s'" % (number)
        cursor.execute(sql)
        result = cursor.fetchall()
        学生名称 = result[0][0]
        # 在t5教师表中查询对应教师编号的教师姓名
        sql = "select 教师姓名 from t5教师信息表 where 教师号='%s'" % (teacher_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        teacher_name = result[0][0]
        # 在t7排课管理表中所对应的教室号
        sql = "select 教室号 from t7排课管理表 where 课程号='%s'" % (course_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        classroom_number = result[0][0]
        # 在t6教室信息表中查询对应教室编号的教室名称和所在位置
        sql = "select 教室名称, 所在位置 from t6教室信息表 where 教室号='%s'" % (classroom_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        classroom_name = result[0][0]
        classroom_location = result[0][1]
        add_course(course_number, number, 课程名称, 学生名称, 1, 1)
    # 查询课程信息
    sql = "select * from t1课程信息表"
    cursor.execute(sql)
    result = cursor.fetchall()
    course_name_list = [r[1] for r in result]
    var = tk.StringVar()
    var.set(course_name_list[0])
    course_name = tk.OptionMenu(select_course_window, var, *course_name_list)
    course_name.place(x=50, y=50)
    sql = "select * from t8登录信息表 where 学号='%s'" % (number)
    cursor.execute(sql)
    result = cursor.fetchall()
    course_number = var.get()
    # 获取下拉框中的课程号，保留为course_number
    add_button = tk.Button(select_course_window, text="添加", command=add_course_func)
    add_button.place(x=100, y=300)
    add_button = tk.Button(select_course_window, text="退课", command=delete_course_func)
    add_button.place(x=150, y=300)
    #在t8登录信息表 查找对应的学号/工号，保留为number
    #在t6教室信息管理中，查找课程号course_number对的教室号，记录为Classroom_numbner，将教室名称记为classroom_name，将教室位置记为classroom_location
    sql = "select 教室号 from t7排课管理表 where 课程号='%s'" % (course_number)
    cursor.execute(sql)
    result = cursor.fetchall()
    classroom_number = result[0][0]
    classroom_name = result[0][1]
    classroom_location = result[0][2]
    #在t7排课管理表中。查找Classroom_number对应的教室号，教师号，保留为room_number，teacher_number，将上课时间记录为class_time
    sql = "select 教室号, 教师号 from t7排课管理表 where 课程号='%s'" % (course_number)
    cursor.execute(sql)
    result = cursor.fetchall()
    classroom_number = result[0][2]
    teacher_number = result[0][1]
    class_time = result[0][3]
    #在t5教师信息表中，查找teacher_number对应的教师姓名，保留为teacher_name
    sql = "select 教师姓名 from t5教师信息表 where 教师号='%s'" % (teacher_number)
    cursor.execute(sql)
    result = cursor.fetchall()
    teacher_name = result[0][1]

    #创建文本框，展示teacher_name，classroom_name，classroom_location，class_time
    teacher_name_label = tk.Label(select_course_window, text="教师姓名：%s" % (teacher_name))
    teacher_name_label.place(x=50, y=100)
    classroom_name_label = tk.Label(select_course_window, text="教室名称：%s" % (classroom_name))
    classroom_name_label.place(x=50, y=150)
    classroom_location_label = tk.Label(select_course_window, text="教室位置：%s" % (classroom_location))
    classroom_location_label.place(x=50, y=200)
    class_time_label = tk.Label(select_course_window, text="上课时间：%s" % (class_time))
    class_time_label.place(x=50, y=250)
    select_course_window.mainloop()#选课退课
def student_course_window(number):#当前课表的创建
    select_course_window = tk.Toplevel()
    select_course_window.title("选课界面")
    select_course_window.geometry("600x400")

    def add_course_func():
        course_name = var.get()
        sql = "select 课程号 from t1课程信息表 where 课程名称='%s'" % (course_name)
        cursor.execute(sql)
        result = cursor.fetchall()
        course_number = result[0][0]
        #在t1课程信息表中查询课程名称为course_name的课程号，保留为course_number
        # 在t7排课管理表中所对应的教师号
        sql = "select 教师号 from t7排课管理表 where 课程号='%s'" % (course_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        teacher_number = result[0]
        # 在t5教师表中查询对应教师编号的教师姓名
        sql = "select 教师名称 from t5教师信息表 where 教师号='%s'" % (teacher_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        teacher_name = result[0]
        # 在t7排课管理表中所对应的教室号
        sql = "select 教室号 from t7排课管理表 where 课程号='%s'" % (course_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        classroom_number = result[0]
        # 在t6教室信息表中查询对应教室编号的教室名称和所在位置
        sql = "select * from t6教室信息表 where 教室号='%s'" % (classroom_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        classroom_name = result[0][1]
        classroom_location = result[0][2]
        #在t2学生信息表中查询对应学号的学生姓名，保存为student_name
        sql = "select 学生名称 from t2学生信息表 where 学号='%s'" % (number)
        cursor.execute(sql)
        result = cursor.fetchall()
        student_name = result[0][0]
        tk.Label(select_course_window, text=course_number).place(x=50, y=100)
        tk.Label(select_course_window, text=teacher_name).place(x=50, y=130)
        tk.Label(select_course_window, text=classroom_name).place(x=50, y=160)
        tk.Label(select_course_window, text=classroom_location).place(x=50, y=190)
        #添加判断，如果此时的课程号，学号，课程名称，学生名称，学分都 正确，则进行添加
        if (course_number!=0 and number !=0 and course_name!=0 ):
            add_course(course_number, number, course_name,student_name,1,1)  # 实现选课功能
        else:
            tk.messagebox.showinfo(title='错误', message='选课失败，请重新选课！')
    def delete_course_func():
        course_name = var.get()
        sql = "select 课程号 from t1课程信息表 where 课程名称='%s'" % (course_name)
        cursor.execute(sql)
        result = cursor.fetchall()
        course_number = result[0][0]
        delete_course(course_number, number)  # 实现退课功能
    #设置按钮，名称为退课，点击后执行 delete_course_func 函数
    tk.Button(select_course_window, text="退课", command=delete_course_func).place(x=200, y=300)

    # 查询课程信息
    sql = "select * from t1课程信息表"
    cursor.execute(sql)
    result = cursor.fetchall()
    course_name_list = [r[1] for r in result]

    var = tk.StringVar()
    var.set(course_name_list[0])

    course_name = tk.OptionMenu(select_course_window, var, *course_name_list)
    course_name.place(x=50, y=50)

    add_button = tk.Button(select_course_window, text="添加", command=add_course_func)
    add_button.place(x=100, y=300)
    #创建表格
    tree = ttk.Treeview(select_course_window, show="headings", height=18, columns=("课程号", "课程名称", "教师名称", "教室名称", "教室位置", "上课时间","起始周次", "结束周次"))
    tree.column("课程号", width=100, anchor='center')
    tree.column("课程名称", width=100, anchor='center')
    tree.column("教师名称", width=100, anchor='center')
    tree.column("教室名称", width=100, anchor='center')
    tree.column("教室位置", width=100, anchor='center')
    tree.column("上课时间", width=100, anchor='center')
    tree.column("起始周次", width=100, anchor='center')
    tree.column("结束周次", width=100, anchor='center')
    tree.heading("课程号", text="课程号")
    tree.heading("课程名称", text="课程名称")
    tree.heading("教师名称", text="教师名称")
    tree.heading("教室名称", text="教室编号")
    tree.heading("教室位置", text="教室位置")
    tree.heading("上课时间", text="上课时间")
    tree.heading("起始周次", text="起始周次")
    tree.heading("结束周次", text="结束周次")


    tree.place(x=300, y=20)
    #在300*500处创建一个表，用于进行“当前课表”的信息展示，表中包含课程名称，教师名称，上课时间，教室名称，教室位置
    def now(number):
        #清空tree
        x = tree.get_children()
        for item in x:
            tree.delete(item)

        #在t4选课信息表中查询此 number对应 学号 的所有课程号，课程名称，保留为Class_number，Class_name
        sql = "select * from t4选课信息表 where 学号='%s'" % (number)
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in range(len(result)):
            course_number = result[i][0]
            sql = "select * from t1课程信息表 where 课程号='%s'" % (course_number)
            cursor.execute(sql)
            result1 = cursor.fetchall()
            course_name = result1[0][1]
            sql = "select * from t7排课管理表 where 课程号='%s'" % (course_number)
            # 在t7表中查询教室号对应的教室名和教室位置
            cursor.execute(sql)
            result2 = cursor.fetchall()
            classroom_number = result2[0][2]
            sql = "select * from t6教室信息表 where 教室号='%s'" % (classroom_number)
            cursor.execute(sql)
            result3 = cursor.fetchall()
            classroom_name = result3[0][0]
            classroom_location = result3[0][1]
            # 在t5教师信息表中查询教师号对应的教师名称
            teacher_number = result2[0][1]
            sql = "select * from t5教师信息表 where 教师号='%s'" % (teacher_number)
            cursor.execute(sql)
            result2 = cursor.fetchall()
            teacher_name = result2[0][1]
            # 在t7排课管理表中查询上课时间，起始周次，结束周次
            sql = "select * from t7排课管理表 where 课程号='%s'" % (course_number)
            cursor.execute(sql)
            result2 = cursor.fetchall()
            time = result2[0][3]
            start_week = result2[0][6]
            end_week = result2[0][7]

            #将对应信息添加到tree中并显示"课程号", "课程名称", "教师名称", "教室名称", "教室位置", "上课时间"，"起始周次", "结束周次"
            tree.insert("", i, text=i, values=(course_number, course_name, teacher_name, classroom_name, classroom_location, time, start_week, end_week))
    #设置按钮，名称为显示，点击后执行 show_course_func 函数

    #定义“show_course_func”函数，调用时关闭现在的所有窗口，并重新进行student_course_window(number)的调用
    def show_course_func():
        now(number)
    show_button = tk.Button(select_course_window, text="显示", command=show_course_func)
    show_button.place(x=150, y=300)
    now(number)
    select_course_window.mainloop()
def create_student_window(username):
    student_window = tk.Toplevel()
    student_window.title("学生窗口")
    student_window.geometry("400x400")
    #创建文本框，显示内容为：用户名，在表t8登录信息表中将用户名对应的 学号/工号，用户类型 依次输出
    sql = "select * from t8登录信息表 where 用户名='%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchall()
    number = result[0][3]
    user_type = result[0][2]
    tk.Label(student_window, text="用户名").place(x=20, y=20)
    tk.Label(student_window, text="学号").place(x=20, y=50)
    tk.Label(student_window, text="用户类型").place(x=20, y=80)
    tk.Label(student_window, text=username).place(x=100, y=20)
    tk.Label(student_window, text=number).place(x=100, y=50)
    tk.Label(student_window, text=user_type).place(x=100, y=80)
    #根据学号/工号 查询表 t2学生信息表 ，依次显示对应的信息：学号，学生名称，年龄，性别，年级，所属学院，专业，所属班级，已修读学分
    sql = "select * from t2学生信息表 where 学号='%s'" % (number)
    cursor.execute(sql)
    result = cursor.fetchall()
    student_name = result[0][1]
    age = result[0][2]
    sex = result[0][3]
    grade = result[0][4]
    college = result[0][5]
    major = result[0][6]
    class_number = result[0][7]
    credit = result[0][8]
    tk.Label(student_window, text="学生名称").place(x=20, y=110)
    tk.Label(student_window, text="年龄").place(x=20, y=140)
    tk.Label(student_window, text="性别").place(x=20, y=170)
    tk.Label(student_window, text="年级").place(x=20, y=200)
    tk.Label(student_window, text="所属学院").place(x=20, y=230)
    tk.Label(student_window, text="专业").place(x=20, y=260)
    tk.Label(student_window, text="所属班级").place(x=20, y=290)
    tk.Label(student_window, text="已修读学分").place(x=20, y=320)
    tk.Label(student_window, text=student_name).place(x=100, y=110)
    tk.Label(student_window, text=age).place(x=100, y=140)
    tk.Label(student_window,text=sex).place(x=100,y=170)
    tk.Label(student_window,text=grade).place(x=100,y=200)
    tk.Label(student_window,text=college).place(x=100,y=230)
    tk.Label(student_window,text=major).place(x=100,y=260)
    tk.Label(student_window,text=class_number).place(x=100,y=290)
    tk.Label(student_window,text=credit).place(x=100,y=320)

    #进行创建按钮
    select_course_button = tk.Button(student_window, text="选课", command=lambda: student_course_window(number))
    select_course_button.place(x=20, y=350)
    #窗口 选课 的设计：用当前的学号/工号在 t4选课信息表 中进行查询，显示当前学生的选课信息：相符的课程号，学号，课程名称，学分选课状态，
    # 再从t7排课管理表中查询对应课程号的教师号，教室号，上课时间，课程容量，下课时间
    student_window.mainloop()
def create_teacher_window(username):
    teacher_window = tk.Toplevel()
    teacher_window.title("教师窗口")
    teacher_window.geometry("600x400")
    #在窗口中显示教师的信息：用户名，在表t8登录信息表中将用户名对应的 学号/工号，用户类型 依次输出
    sql = "select * from t8登录信息表 where 用户名='%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchall()
    number = result[0][3]
    user_type = result[0][2]
    tk.Label(teacher_window, text="用户名").place(x=20, y=20)
    tk.Label(teacher_window, text="工号").place(x=20, y=50)
    tk.Label(teacher_window, text="用户类型").place(x=20, y=80)
    tk.Label(teacher_window, text=username).place(x=100, y=20)
    tk.Label(teacher_window, text=number).place(x=100, y=50)
    tk.Label(teacher_window, text=user_type).place(x=100, y=80)
    #在t5教师信息表中查询number对应的教师号，显示教师名称，所属学院，专业，年龄
    sql = "select * from t5教师信息表 where 教师号='%s'" % (number)
    cursor.execute(sql)
    result = cursor.fetchall()
    teacher_name = result[0][1]
    college = result[0][2]
    major = result[0][3]
    age = result[0][4]
    tk.Label(teacher_window, text="教师名称").place(x=20, y=110)
    tk.Label(teacher_window, text="所属学院").place(x=20, y=140)
    tk.Label(teacher_window, text="专业").place(x=20, y=170)
    tk.Label(teacher_window, text="年龄").place(x=20, y=200)
    tk.Label(teacher_window, text=teacher_name).place(x=100, y=110)
    tk.Label(teacher_window, text=college).place(x=100, y=140)
    tk.Label(teacher_window, text=major).place(x=100, y=170)
    tk.Label(teacher_window, text=age).place(x=100, y=200)
    #在t7排课管理表中查询教师号对应的课程号，查询对应的上课时间并显示，保留课程号为course_number，保留教室号为room_number
    sql = "select * from t7排课管理表 where 教师号='%s'" % (number)
    cursor.execute(sql)
    result = cursor.fetchall()
    course_number = result[0][0]
    room_number = result[0][2]
    time = result[0][3]
    tk.Label(teacher_window, text="上课信息").place(x=20, y=230)
    tk.Label(teacher_window, text=time).place(x=100, y=230)
    #在t1课程信息表中查询课程号对应的课程名称并显示
    sql = "select * from t1课程信息表 where 课程号='%s'" % (course_number)
    cursor.execute(sql)
    result = cursor.fetchall()
    course_name = result[0][1]
    tk.Label(teacher_window, text="课程名称").place(x=20, y=260)
    #在t6教室信息表中查询教室号对应的教室所在位置并显示，查询教室名并显示
    sql = "select * from t6教室信息表 where 教室号='%s'" % (room_number)
    cursor.execute(sql)
    result = cursor.fetchall()
    room_location = result[0][2]
    room_name = result[0][1]
    tk.Label(teacher_window, text=room_location).place(x=100, y=230)
    tk.Label(teacher_window, text="教室位置").place(x=20, y=230)
    tk.Label(teacher_window, text=room_name).place(x=100, y=260)
    tk.Label(teacher_window, text="教室名称").place(x=20, y=260)
    #显示课程名称course_name
    tk.Label(teacher_window, text=course_name).place(x=100, y=290)
    tk.Label(teacher_window, text="课程名称").place(x=20, y=290)
    #创建查询按钮，点击后在t3教学班信息表中查询对应 班主任信息为number 的数据，并以表格的形式显示
    def search():
        sql = "select * from t3教学班信息表 where 班主任信息='%s'" % (number)
        cursor.execute(sql)
        result = cursor.fetchall()
        #创建表格
        tree = ttk.Treeview(teacher_window, show="headings", columns=("a", "b", "c", "d", "e", "f"))
        for i in range(len(result)):
            sql = "select * from t2学生信息表 where 学号='%s'" % (result[i][2])
            cursor.execute(sql)
            result1 = cursor.fetchall()
            student_number= result[0][0]
            student_name = result1[0][1]
            college = result1[0][5]
            major = result1[0][6]
            student_age= result1[0][2]
            student_class = result1[0][7]
            tree.insert("", i, values=(student_number, student_name, major,college,  student_age, student_class)    )
            #显示内容为：学号，学生姓名，专业，学院，年级，班级
        tree.column("a", width=100, anchor="center")
        tree.column("b", width=100, anchor="center")
        tree.column("c", width=100, anchor="center")
        tree.column("d", width=100, anchor="center")
        tree.column("e", width=100, anchor="center")
        tree.column("f", width=100, anchor="center")
        tree.heading("a", text="学号")
        tree.heading("b", text="学生姓名")
        tree.heading("c", text="专业")
        tree.heading("d", text="学院")
        tree.heading("e", text="年级")
        tree.heading("f", text="班级")

        tree.place(x=20, y=350)
    #创建查询按钮
    tk.Button(teacher_window, text="查询教学班信息", command=search).place(x=20, y=320)

    #创建查询按钮，点击后查询教室信息
    def search_room():
        #在t7排课信息表中检索所有教室号为RID
        sql = "select * from t7排课管理表 where 教室号='%s'" % (room_number)
        cursor.execute(sql)
        result = cursor.fetchall()
        RID = []
        for i in range(len(result)):
            RID.append(result[i][2])
        #在t6教室信息表中查询所有教室号，记录为RNUM
        sql = "select * from t6教室信息表"
        cursor.execute(sql)
        result = cursor.fetchall()
        RNUM = []
        for i in range(len(result)):
            RNUM.append(result[i][0])
        #对比RNUM和RID，如果只在RNUM中，则记录其值为1，否则记录状态为2
        status = []
        for i in range(len(RNUM)):
            if RNUM[i] in RID:
                status.append(1)
            else:
                status.append(2)
        #创建表格
        #检索所有状态为2的教室号，并在t7排课管理表中查询 其对应的上课时间，下课时间，记录为STIME，ETIME
        tree = ttk.Treeview(teacher_window, show="headings", columns=("a", "b", "c", "d", "e"))
        for i in range(len(status)):
            if status[i] == 2:
                sql = "select * from t7排课管理表 where 教室号='%s'" % (RNUM[i])
                cursor.execute(sql)
                result = cursor.fetchall()
                STIME = result[0][3]
                ETIME = result[0][5]
                tree.insert("", i, values=(RNUM[i], STIME, ETIME))
        #所有状态为1的教室号，记录ETIME=0，STIME=0
        for i in range(len(status)):
            if status[i] == 1:
                tree.insert("", i, values=(RNUM[i], 0, 0))
        tree.column("a", width=100, anchor="center")
        tree.column("b", width=100, anchor="center")
        tree.column("c", width=100, anchor="center")
        tree.column("d", width=100, anchor="center")
        tree.column("e", width=100, anchor="center")
        tree.heading("a", text="教室号")
        tree.heading("b", text="上课时间")
        tree.heading("c", text="下课时间")
        tree.place(x=150, y=350)
    tk.Button(teacher_window, text="查询教室信息", command=search_room).place(x=150, y=320)

    teacher_window.mainloop()


def create_manager_window(username):
    manager_window = tk.Toplevel()
    manager_window.title("管理员窗口")
    manager_window.geometry("1000x600")
    table_name = tk.StringVar()
    row_name = tk.StringVar()
    column_name = tk.StringVar()
    TABLE_NAME=table_name
    tk.Label(manager_window, text="管理员窗口").place(x=20, y=00)
    tk.Label(manager_window, text="选择数据表").place(x=20, y=20)
    #在下拉框中选择数据表名
    table_name_chosen = ttk.Combobox(manager_window, width=12, textvariable=table_name)
    table_name_chosen['values'] = ('t1课程信息表', 't2学生信息表', 't3教学班信息表', 't4选课信息表', 't5教师信息表', 't6教室信息表', 't7排课管理表', 't8登录信息表','t9选科条件表')
    table_name_chosen.place(x=100, y=00)
    table_name_chosen.current(0)
    TABLENAME=TABLE_NAME.get()
    def tn1():

        #创建输入框，依次为：课程号，课程名称，课程类别，开课学院，学分，课时，限制
        tk.Label(manager_window, text="课程号").place(x=20, y=50)
        tk.Label(manager_window, text="课程名称").place(x=20, y=80)
        tk.Label(manager_window, text="课程类别").place(x=20, y=110)
        tk.Label(manager_window, text="开课学院").place(x=20, y=140)
        tk.Label(manager_window, text="学分").place(x=20, y=170)
        tk.Label(manager_window, text="课时").place(x=20, y=200)
        tk.Label(manager_window, text="限制").place(x=20, y=230)
        t1_1 = tk.StringVar()
        t1_2 = tk.StringVar()
        t1_3 = tk.StringVar()
        t1_4 = tk.StringVar()
        t1_5 = tk.StringVar()
        t1_6 = tk.StringVar()
        t1_7 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t1_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t1_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t1_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t1_4).place(x=100, y=140)
        tk.Entry(manager_window, textvariable=t1_5).place(x=100, y=170)
        tk.Entry(manager_window, textvariable=t1_6).place(x=100, y=200)
        tk.Entry(manager_window, textvariable=t1_7).place(x=100, y=230)

        #创建添加按钮，点击后在t1表中添加对应数据
        def add_t1():#给对应的 课程号，课程名称，课程类别，开课学院，学分，课时，限制 列，加入 t1_1.get(), t1_2.get(), t1_3.get(), t1_4.get(), t1_5.get(), t1_6.get(), t1_7.get()
            sql = "insert into t1课程信息表(课程号,课程名称,课程类别,开课学院,学分,课时,限制) values('%s','%s','%s','%s','%s','%s','%s')" % (t1_1.get(), t1_2.get(), t1_3.get(), t1_4.get(), t1_5.get(), t1_6.get(), t1_7.get())
            #执行sql语句
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()

        tk.Button(manager_window, text="添加", command=add_t1).place(x=330, y=20)
        def delete_t1():
            sql = "delete from t1课程信息表 where 课程号='%s'" % (t1_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        #创建删除按钮，点击后在t1表中删除对应数据
        tk.Button(manager_window, text="删除", command=delete_t1).place(x=380, y=20)
    def tn2(): #创建输入框，输入内容依次为学号，学生名称，年龄，性别，年级，所属学院，专业，所属班级，已修读学分
        tk.Label(manager_window, text="学号").place(x=20, y=50)
        tk.Label(manager_window, text="学生名称").place(x=20, y=80)
        tk.Label(manager_window, text="年龄").place(x=20, y=110)
        tk.Label(manager_window, text="性别").place(x=20, y=140)
        tk.Label(manager_window, text="年级").place(x=20, y=170)
        tk.Label(manager_window, text="所属学院").place(x=20, y=200)
        tk.Label(manager_window, text="专业").place(x=20, y=230)
        tk.Label(manager_window, text="所属班级").place(x=20, y=260)
        tk.Label(manager_window, text="已修读学分").place(x=20, y=290)
        t2_1 = tk.StringVar()
        t2_2 = tk.StringVar()
        t2_3 = tk.StringVar()
        t2_4 = tk.StringVar()
        t2_5 = tk.StringVar()
        t2_6 = tk.StringVar()
        t2_7 = tk.StringVar()
        t2_8 = tk.StringVar()
        t2_9 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t2_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t2_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t2_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t2_4).place(x=100, y=140)
        tk.Entry(manager_window, textvariable=t2_5).place(x=100, y=170)
        tk.Entry(manager_window, textvariable=t2_6).place(x=100, y=200)
        tk.Entry(manager_window, textvariable=t2_7).place(x=100, y=230)
        tk.Entry(manager_window, textvariable=t2_8).place(x=100, y=260)
        tk.Entry(manager_window, textvariable=t2_9).place(x=100, y=290)
        #创建添加按钮，点击后在t2表中添加对应数据
        def add_t2():
            sql = "insert into t2学生信息表 values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (t2_1.get(), t2_2.get(), t2_3.get(), t2_4.get(), t2_5.get(), t2_6.get(), t2_7.get(), t2_8.get(), t2_9.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="添加", command=add_t2).place(x=330, y=20)
        #创建删除按钮，点击后在t2表中删除对应数据
        def delete_t2():
            sql = "delete from t2学生信息表 where 学号='%s'" % (t2_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="删除", command=delete_t2).place(x=380, y=20)
    def tn3(): #创建输入框，输入内容依次为教学班号，教学班名称，学生信息，班主任信息，课程类型
        tk.Label(manager_window, text="教学班号").place(x=20, y=50)
        tk.Label(manager_window, text="教学班名称").place(x=20, y=80)
        tk.Label(manager_window, text="学生信息").place(x=20, y=110)
        tk.Label(manager_window, text="班主任信息").place(x=20, y=140)
        tk.Label(manager_window, text="课程类型").place(x=20, y=170)
        t3_1 = tk.StringVar()
        t3_2 = tk.StringVar()
        t3_3 = tk.StringVar()
        t3_4 = tk.StringVar()
        t3_5 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t3_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t3_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t3_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t3_4).place(x=100, y=140)
        tk.Entry(manager_window, textvariable=t3_5).place(x=100, y=170)
        #创建添加按钮，点击后在t3表中添加对应数据
        def add_t3():
            sql = "insert into t3教学班信息表 values('%s','%s','%s','%s','%s')" % (t3_1.get(), t3_2.get(), t3_3.get(), t3_4.get(), t3_5.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="添加", command=add_t3).place(x=330, y=20)
        #创建删除按钮，点击后在t3表中删除对应数据
        def delete_t3():
            sql = "delete from t3教学班信息表 where 教学班号='%s'" % (t3_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="删除", command=delete_t3).place(x=380, y=20)
    def tn4():#创建输入框，内容为课程号，学号，课程名称，学生名称，学分，（选课状态，直接插入为成功）
        tk.Label(manager_window, text="课程号").place(x=20, y=50)
        tk.Label(manager_window, text="学号").place(x=20, y=80)
        tk.Label(manager_window, text="课程名称").place(x=20, y=110)
        tk.Label(manager_window, text="学生名称").place(x=20, y=140)
        tk.Label(manager_window, text="学分").place(x=20, y=170)
        t4_1 = tk.StringVar()
        t4_2 = tk.StringVar()
        t4_3 = tk.StringVar()
        t4_4 = tk.StringVar()
        t4_5 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t4_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t4_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t4_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t4_4).place(x=100, y=140)
        tk.Entry(manager_window, textvariable=t4_5).place(x=100, y=170)
        #创建添加按钮，点击后在t4表中添加对应数据
        def add_t4():
            sql = "insert into t4选课信息表 values('%s','%s','%s','%s','%s','成功')" % (t4_1.get(), t4_2.get(), t4_3.get(), t4_4.get(), t4_5.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="添加", command=add_t4).place(x=330, y=20)
        #创建删除按钮，点击后在t4表中删除对应数据
        def delete_t4():
            sql = "delete from t4选课信息表 where 课程号='%s'" % (t4_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="删除", command=delete_t4).place(x=380, y=20)
    def tn5():#创建输入框，内容为教师号，教师名称，所属学院，专业，年龄，入职时间
        tk.Label(manager_window, text="教师号").place(x=20, y=50)
        tk.Label(manager_window, text="教师名称").place(x=20, y=80)
        tk.Label(manager_window, text="所属学院").place(x=20, y=110)
        tk.Label(manager_window, text="专业").place(x=20, y=140)
        tk.Label(manager_window, text="年龄").place(x=20, y=170)
        tk.Label(manager_window, text="入职时间").place(x=20, y=200)
        t5_1 = tk.StringVar()
        t5_2 = tk.StringVar()
        t5_3 = tk.StringVar()
        t5_4 = tk.StringVar()
        t5_5 = tk.StringVar()
        t5_6 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t5_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t5_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t5_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t5_4).place(x=100, y=140)
        tk.Entry(manager_window, textvariable=t5_5).place(x=100, y=170)
        tk.Entry(manager_window, textvariable=t5_6).place(x=100, y=200)
        #创建添加按钮，点击后在t5表中添加对应数据
        def add_t5():
            sql = "insert into t5教师信息表 values('%s','%s','%s','%s','%s','%s')" % (t5_1.get(), t5_2.get(), t5_3.get(), t5_4.get(), t5_5.get(), t5_6.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="添加", command=add_t5).place(x=330, y=20)
        #创建删除按钮，点击后在t5表中删除对应数据
        def delete_t5():
            sql = "delete from t5教师信息表 where 教师号='%s'" % (t5_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="删除", command=delete_t5).place(x=380, y=20)
    def tn6():#创建输入框，内容为教室号，教室名，所在位置，教室容量
        tk.Label(manager_window, text="教室号").place(x=20, y=50)
        tk.Label(manager_window, text="教室名").place(x=20, y=80)
        tk.Label(manager_window, text="所在位置").place(x=20, y=110)
        tk.Label(manager_window, text="教室容量").place(x=20, y=140)
        t6_1 = tk.StringVar()
        t6_2 = tk.StringVar()
        t6_3 = tk.StringVar()
        t6_4 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t6_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t6_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t6_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t6_4).place(x=100, y=140)
        #创建添加按钮，点击后在t6表中添加对应数据
        def add_t6():
            sql = "insert into t6教室信息表 values('%s','%s','%s','%s')" % (t6_1.get(), t6_2.get(), t6_3.get(), t6_4.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="添加", command=add_t6).place(x=330, y=20)
        #创建删除按钮，点击后在t6表中删除对应数据
        def delete_t6():
            sql = "delete from t6教室信息表 where 教室号='%s'" % (t6_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="删除", command=delete_t6).place(x=380, y=20)
    def tn7():#创建输入框，内容为课程号，教师号，教室号，上课时间，课程容量，下课时间
        tk.Label(manager_window, text="课程号").place(x=20, y=50)
        tk.Label(manager_window, text="教师号").place(x=20, y=80)
        tk.Label(manager_window, text="教室号").place(x=20, y=110)
        tk.Label(manager_window, text="上课时间").place(x=20, y=140)
        tk.Label(manager_window, text="课程容量").place(x=20, y=170)
        tk.Label(manager_window, text="下课时间").place(x=20, y=200)
        t7_1 = tk.StringVar()
        t7_2 = tk.StringVar()
        t7_3 = tk.StringVar()
        t7_4 = tk.StringVar()
        t7_5 = tk.StringVar()
        t7_6 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t7_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t7_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t7_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t7_4).place(x=100, y=140)
        tk.Entry(manager_window, textvariable=t7_5).place(x=100, y=170)
        tk.Entry(manager_window, textvariable=t7_6).place(x=100, y=200)
        #创建添加按钮，点击后在t7表中添加对应数据
        def add_t7():
            sql = "insert into t7排课管理表 values('%s','%s','%s','%s','%s','%s')" % (t7_1.get(), t7_2.get(), t7_3.get(), t7_4.get(), t7_5.get(), t7_6.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="添加", command=add_t7).palce(x=330, y=20)
        #创建删除按钮，点击后在t7表中删除对应数据
        def delete_t7():
            sql = "delete from t7排课管理表 where 课程号='%s'" % (t7_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="删除", command=delete_t7).place(x=380, y=20)
    def tn8():#创建输入框，内容为用户名，密码，用户类型，学号/工号
        tk.Label(manager_window, text="用户名").place(x=20, y=50)
        tk.Label(manager_window, text="密码").place(x=20, y=80)
        tk.Label(manager_window, text="用户类型").place(x=20, y=110)
        tk.Label(manager_window, text="学号/工号").place(x=20, y=140)
        t8_1 = tk.StringVar()
        t8_2 = tk.StringVar()
        t8_3 = tk.StringVar()
        t8_4 = tk.StringVar()
        tk.Entry(manager_window, textvariable=t8_1).place(x=100, y=50)
        tk.Entry(manager_window, textvariable=t8_2).place(x=100, y=80)
        tk.Entry(manager_window, textvariable=t8_3).place(x=100, y=110)
        tk.Entry(manager_window, textvariable=t8_4).place(x=100, y=140)
        #创建添加按钮，点击后在t8表中添加对应数据
        def add_t8():
            sql = "insert into t8登录信息表 values('%s','%s','%s','%s')" % (t8_1.get(), t8_2.get(), t8_3.get(), t8_4.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="添加", command=add_t8).place(x=330, y=20)
        #创建删除按钮，点击后在t8表中删除对应数据
        def delete_t8():
            sql = "delete from t8登录信息表 where 用户名='%s'" % (t8_1.get())
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        tk.Button(manager_window, text="删除", command=delete_t8).place(x=380, y=20)
    def tn9():
        pass
    def flash():
        TABLENAME=table_name.get()
        #如果TABLENAME=t1课程信息表', 't2学生信息表', 't3教学班信息表', 't4选课信息表', 't5教师信息表', 't6教室信息表', 't7排课管理表', 't8登录信息表','t9选科条件表'中的一个，则跳转到对应的tn函数
        if TABLENAME=='t1课程信息表':
            tn1()
        elif TABLENAME=='t2学生信息表':
            tn2()
        elif TABLENAME=='t3教学班信息表':
            tn3()
        elif TABLENAME=='t4选课信息表':
            tn4()
        elif TABLENAME=='t5教师信息表':
            tn5()
        elif TABLENAME=='t6教室信息表':
            tn6()
        elif TABLENAME=='t7排课管理表':
            tn7()
        elif TABLENAME=='t8登录信息表':
            tn8()
        elif TABLENAME=='t9选科条件表':
            tn9()

    def show_table():
        table_name = TABLE_NAME.get()
        sql = "select * from %s" % (table_name)
        cursor.execute(sql)
        result = cursor.fetchall()

        # 获取表的列名
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % (table_name)
        cursor.execute(sql)
        result1 = cursor.fetchall()
        column_name = [row[0] for row in result1]

        # 创建表格
        tree = ttk.Treeview(manager_window, show="headings", columns=column_name)

        # 设置表格每列的宽度
        for i in range(len(column_name)):
            tree.column(column_name[i], width=100, anchor='center')

        # 设置表格每列表头的名称
        for i in range(len(column_name)):
            tree.heading(column_name[i], text=column_name[i])

        # 插入数据
        for row in result:
            tree.insert('', 'end', values=row)
        #调整表格大小为300*600，位置在300*300处
        tree.place(x=300, y=300, width=600, height=300)

    tk.Button(manager_window, text="显示表格", command=show_table,bg="yellow").place(x=200, y=20)

    #创建按钮，点击后调用flash函数
    tk.Button(manager_window, text="刷新", command=flash,bg="red").place(x=280, y=20)
    #设置按钮颜色为蓝色
    manager_window.mainloop()

def create_main_window():
    def usr_login():
        usr_name = var_usr_name.get()
        usr_pwd = var_usr_pwd.get()
        sql = "SELECT * FROM t8登录信息表 WHERE 用户名='%s' AND 密码='%s'" % (usr_name, usr_pwd)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
   #         print("登录成功")
            usr_type()  # 获取用户类型
     #   else:
      #      print("错误")

    def usr_type():
        usr_name = var_usr_name.get()
        sql = "SELECT 用户类型 FROM t8登录信息表 WHERE 用户名='%s'" % usr_name
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            #user_type = result  # 获取用户类型
            user_type = result[0]
            username = var_usr_name.get()
            if user_type == "student":
                create_student_window(username)
                #关闭当前的main窗口
            elif user_type == "teacher":
                create_teacher_window(username)
                #关闭当前的main窗口
            elif user_type == "manager":
                create_manager_window(username)
                #关闭当前的主窗口
            else:
                print("错误")

    main_window = tk.Tk()
    main_window.title("主窗口")
    main_window.geometry("400x400")

    tk.Label(main_window, text="用户名").place(x=50, y=150)
    tk.Label(main_window, text="密码").place(x=50, y=190)
    var_usr_name = tk.StringVar()
    var_usr_name.set("admin")
    var_usr_pwd = tk.StringVar()
    entry_usr_name = tk.Entry(main_window, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=150)
    entry_usr_pwd = tk.Entry(main_window, textvariable=var_usr_pwd, show="*")
    entry_usr_pwd.place(x=160, y=190)

    btn_login = tk.Button(main_window, text="提交", command=usr_login,bg="yellow")
    btn_login.place(x=170, y=230)

    main_window.mainloop()
create_main_window()