---
layout: post
lang: vn
title: Tự động hóa định dạng văn bản với Word
author: Phan-Canh Trinh 
link: 
---

Có lẽ một số bạn rất ghét các tính năng tự động của MS. Word; nhiều khi nó tỏ ra thật phiền toái. Đại loại như tự động đặt Bullet, tự động xuống dòng, tự động thêm dấu cách... Tuy nhiên, khi thiết kế phần mềm hẳn là nhà sản xuất đã có dụng ý, nghiên cứu kỹ nhu cầu người dùng để đưa ra chúng. Vậy tại sao chúng ta không nghĩ sẽ làm chủ tính năng tự động đó để phục vụ mình một cách tối ưu.

Bài viết sau sẽ trình bày một số thủ thuật để tự động hóa quá trình định dạng văn bản trong MS Word 2013. Sẽ hoàn toàn tương tự cho các phiên bản khác.

**1.Thiết lập lại một số mặc định cơ bản**

**1.1. Thiết lập trangFile/ Print/ Page Setup** hoặc nhấp đôi vào **thanh Ruler** để hiển thị hộp thoại Page Setup. Đặt các thông số cần thiết: Lề và gáy đặt ở Tab Margin; khổ giấy A4 ở Tab Paper. 

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic1.png)

Lưu ý: Nút **Set As Default** ở góc trái cuối hộp thoại cho phép mặc định lại các thông số đã đặt cho những file sau này, nếu các thông số sử dụng thường xuyên các bạn có thể nhấn nút này.

**1.2. Thiết lập font chữ mặc định**

Truy cập Tab **Design/ Font/ Customize Font...** xuất hiện hộp thoại bên dưới, chọn font chữ bạn cần (thường chúng ta sử dụng Time New Roman, ở đây có 2 ô để mặc định cho tiêu đề và cho nội dung); đặt tên cho định dạng mới này; kích nút **Save** để lưu lại.

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic2.png)

**1.3. Làm chủ các định dạng mẫu**

*1.3.1. Tiêu đề*

Giả sử chúng ta có bố cục bài báo cáo với yêu cầu như sau:

1. TIÊU ĐỀ CẤP 1               : cỡ 16, kiểu hoa, in đậm

1.1. TIÊU ĐỀ CẤP 2            : cỡ 14, kiểu hoa và đậm

1.1.1.Tiêu đề cấp 3              : cỡ 14, kiểu thường và đậm

1.1.1.1.Tiêu đề cấp 4           : cỡ 14, kiểu thường

Đặt con trỏ chuột tại dòng Tiêu đề 1, chọn Numbering với thể loại như hình sau. Tương tự cho tiêu đề cấp 2, 3, 4. Để **lùi cấp cho tiêu đề**, kích chuột vào Numbering của tiêu đề vừa tạo, nhấn phím **Tab**.

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic3.png)

**Chìa khóa:** MS Word mặc định đằng sau Numbering hay Bullet là một ký tự Tab, do vậy khoảng cách này khá dài và thay đổi bất thường tùy vào chuỗi ký tự theo sau. Cách loại bỏ như sau:

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic4.png)

Đặt lại cách lề cho tiêu đề tùy mục đích của bạn, mình đặt lại 0 cm. 
Kích **Set for All Levels** nếu muốn áp dụng tất cả các cấp.

Kích nút **More/Less** ở góc trái dưới cùng hộp thoại, bạn sẽ thấy phần mở rộng. Chuyển thuộc tính **Follow number with:** thành **Space** (1 dấu cách theo sau Number).

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic5.png)

Sau khi hoàn thành, các bạn tiếp tục định dạng cỡ chữ, màu chữ, font chữ cho tiêu đề nếu cần. Bước tiếp theo là lưu lại mẫu tiêu đề để áp dụng cho các tiêu đề khác. Quá trình được mô tả như sau:

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic6.png)

Chọn tiêu cấp 1 đã định dạng, kích chuột phải vào **Heading 1** trên thanh công cụ, chọn **Update Heading 1...** để lưu lại thuộc tính đã định dạng.

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic7.png)

Di chuyển đến 1 tiêu đề khác cùng cấp kích **Heading 1** để áp dụng định dạng đã lưu. Làm tương tự cho **Heading 2, 3, 4**...

*1.3.2. Tự động tạo mục lục hình ảnh, bảng biểu

*Để mục lục hình ảnh và bảng biểu được tạo một cách tự động, đòi hỏi chúng ta phải làm đúng từ thao tác nhập liệu.

*Tạo tên bảng, tên hình kèm số thứ tự*

Chúng ta có tài liệu gồm bảng và hình như sau, trước hết chúng ta thực hiện thao tác đặt tên hình, bảng (**Lưu ý:** thao tác này giúp số thứ tự hình, bảng tự động cập nhật về sau).

Kích chuột phải, chọn **Insert Caption/ New Label,** đặt tên cho Label mới là (Bảng/ Hình), bấm OK.

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic8.png)

Chọn lại vị trí của Tên bảng (thường quy định nằm trên, tên hình nằm dưới); Điền tên Bảng/ Hình vào mục Caption. Xong các bạn nhấn OK.

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic9.png)

Đến đây, STT của Bảng/ Hình sẽ được tự động cập nhật; có nghĩa là nếu bạn thêm một bảng vào phía trước bảng đã tạo, Word sẽ tự động đánh lại STT đúng cho bạn. Trường hợp STT không được tự động sửa lại các bạn làm như sau:

Kích phải vào **STT Bảng/Update Field**

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic10.png)

*Tạo mục lục hình ảnh, bảng biểu*

Trước hết, bạn định dạng lại font chữ, cỡ chữ, màu sắc cho tiêu đề bảng/ hình. Sau đó, lưu lại Style này để áp dụng cho các bảng khác.

Cách làm như sau:

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic11.png)

Bước tiếp theo là tiến hành tạo mục lục hình ảnh, bảng biểu:

Đặt vị trí trỏ chuột tại nơi muốn xuất mục lục.

Chọn mục **References**/ Kích chọn **Insert Table of Figures**

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic12.png)

Một hộp thoại xuất hiện như hình bên dưới.\
Chọn Formats là **From Template** để lấy định dạng từ tên bảng đã thực hiện.\
Chọn Caption label là Bảng sẽ được mục lục bảng, Hình sẽ được mục lục hình.\
Chọn Include label and number để xác định Label có xuất hiện cùng mục lục hay không (Tức *Bảng 1: Text...,* hay là *1: Text...)*

![](/images/vn_tut/tu-dong-hoa-dinh-dang-word/pic13.png)

Như vậy, chúng ta đã có mục lục tự động cho phần bảng biểu và hình ảnh.

***Cập nhật:*** [Template](https://drive.google.com/file/d/1iHiIY4T-83_Blt2Ctds4JIxs3-BQjeG4/view?usp=sharing) theo yêu cầu Khoa Dược -- Đại học Y Dược Tp. HCM và hướng dẫn Video.

<iframe width="100%" height="500" src="https://www.youtube.com/embed/ggd9kka_eSY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>

</iframe>
