---
layout: post
lang: vn
title: Heading trong Word bị mảng đen biết phải làm sao?
author: Phan-Canh Trinh
link: 
---

Một ngày đẹp trời Khoá luận của bạn mở lên và Heading bị đen lại.

![](/images/vn_tut/header-den-word/p1.png)

Tốt nhất đập đi làm lại\... Lần 1. OK

Lần khác mở lên, đen tiếp\... Đập làm lại\...

Đã bị thì nó sẽ bị hoài\...

Cách giải quyết như sau:

**Bước 1:** Lưu lại 1 file mới cho chắc ăn

**Bước 2:** Trên file mới đang mở tạo Macro như sau:

![](/images/vn_tut/header-den-word/p2.png)

Chọn tiếp Dấu cộng(+) 

![](/images/vn_tut/header-den-word/p3.png)

Cửa sổ mới như sau:

![](/images/vn_tut/header-den-word/p4.png)

Dán đoạn code sau vào:

      Sub RemoveBlackBox()
      '
      ' RemoveBlackBox Macro
      '
      '
      
      For Each templ In ActiveDocument.ListTemplates
      For Each lev In templ.ListLevels
      lev.Font.Reset
      Next lev
      Next templ
      
      End Sub

![](/images/vn_tut/header-den-word/p5.png)

Cuối cùng nhấn Run (Hình tam giác ở góc trái màn hình).\
![](/images/vn_tut/header-den-word/p6.png)

Chờ đoạn code chạy xong thì tắt cửa sổ đi là xong!

Tham khảo từ [superuser.com](https://superuser.com/questions/521659/numbering-in-ms-word-turned-into-black-boxes)
