---
layout: post
lang: vn
title: Hiện file ẩn do virus
author: TrinhPHAN
link: 
---

Virus là một trong những phiền toái lớn của người dùng máy tính; những nỗi khốn đốn này thường đi kèm với anh bạn không thể không nhắc tới là chiếc USB. Lỗi thường gặp nhất là các file trong USB bị sau khi nhiễm virus, nhiều người tá hỏa lên với vấn đề này vì tưởng rằng dữ liệu của họ đã bị gặm nhấm hết. Thật ra các dữ liệu này vẫn còn ở đó chỉ là bị ẩn đi thôi. Đặc điểm các virus này thường khóa luôn chức năng hiện file trong **Folder Option** nên khó lòng lấy lại được dễ dàng. Những trường hợp cấp bách như vậy chúng ta có thể áp dụng một số cách sau:

**Cách 1. Thử hiện file trong Folder Option**

Đặt các thuộc tính như hình bên dưới, lưu ý mục **Hide protected operating system files...** không được chọn. Cuối cùng nhấn OK và xem kết quả.

![](/images/vn_tut/hien-virus/p1.jpg)

![](/images/vn_tut/hien-virus/p2.jpg)

**Cách 2. Gõ lệnh hiện file vào cmd**\
Bấm Window + R để mở lệnh Run...Nhập cmd. Bấm Enter.

![](/images/vn_tut/hien-virus/p3.jpg)

Cửa sổ **Command Prompt** hiện ra. Tiếp đến gõ lệnh **F:** (lưu ý F là ổ USB của bạn) và nhấn Enter để chuyển dấu nhắc sang ổ USB.Gõ lệnh **attrib -S -H /S /D** và nhấn Enter là xong.**Lưu ý:**-S để bỏ đi thuộc tính hệ thống bị khóa.-H là bỏ đi thuộc tính ẩn bị khóa./S, /D có chức năng thay đổi thuộc tính cho tất cả file, thư mục trong ổ USB.

**Cách 3. Sử dụng phần mềm Bkav FixAttrb hoặc USB Show**

[**Download**](https://drive.google.com/file/d/0B8Hrctiq-vGRUTdFZnhBQjdxc0U/view?usp=sharing)

Sau khi tải về các bạn chạy file lên và sử dụng, giao diện phần mềm cực kỳ đơn giản như sau:

![](/images/vn_tut/hien-virus/p4.jpg)

![](/images/vn_tut/hien-virus/p5.jpg)

Chọn thư mục hoặc ổ đĩa cần hiện file ẩn. Ấn OK. Sau đó bấm Hiện file ẩn là xong.

![](/images/vn_tut/hien-virus/p6.jpg)

![](/images/vn_tut/hien-virus/p7.jpg)

**Với Bkav FixAttrb.exe:** bạn click vào \"**Chọn ổ đĩa**\" để chọn ổ đĩa hoặc thư mục cần hiện các file ẩn rồi bấm \"**OK**\", công cụ báo \"**Đã đặt xong thuộc tính!**\". Lúc này, các bạn đóng cửa sổ công cụ lại, rồi vào ổ đĩa kiểm tra thử xem các file và thư mục bị ẩn giờ đã có thể truy nhập và nhìn thấy dữ liệu bị ẩn trước đó chưa nhé.

**Với USB Show.exe:** trên giao diện chính bạn bấm nút **\"Recovery the hide files\"**, ở cửa sổ **\"Browse For Folder\"** tìm chọn ổ đĩa USB mà bạn cần thực hiện, rồi bấm **\"OK\"**. Quá trình quét và khôi phục file bị virus ẩn đi sẽ diễn ra sau đó. Đến khi hoàn tất, bạn bấm OK.
