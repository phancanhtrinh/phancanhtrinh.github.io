---
layout: diary_post
title: "Tự động hóa định dạng văn bản với Word [Kỳ 1]"
date: 2015-01-06T23:28:00.001000+07:00
categories:
  - diary
permalink: /diary/2015/01/06/t-ng-h-a-nh-d-ng-v-n-b-n-v-i-word-k-1/
source_url: "https://phancanhtrinh.blogspot.com/2015/01/tu-ong-hoa-viec-inh-dang-van-ban-voi.html"
summary: "Có lẽ một số bạn rất ghét các tính năng tự động của MS. Word; nhiều khi nó tỏ ra thật phiền toái. Đại loại như tự động đặt Bullet, tự động xuống dòng, tự động thêm dấu cách… Tuy nhiên, khi thiết kế phần mềm hẳn là nhà sản xuất đã có dụng ý, nghiên cứu kỹ nhu cầu người dùng để đưa ra chúng. Vậy tại sao chúng ta không nghĩ sẽ làm chủ tính năng tự động đó để phục vụ mình một cách tối ưu. Bài viết sau sẽ trình bày một số thủ thuật để tự động hóa quá trình định dạng văn bản trong MS Word 2013. Sẽ hoà"
thumbnail: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjX_Ao5xbyKQ4m2X4XkOahNM6m31Gxe5yCDliR_kp90OmqN7NPNYxcSZND66anlrC4CFLTuemoafl1-lv9CJNBenEGdrgpoWLy5VPmoUjHty_sHgkbcYcjG291eHnjPrVv9XN3i3LZEFx8/s1600/Picture1.png"
---
Có lẽ một số bạn rất ghét các tính năng tự động của MS. Word; nhiều khi nó tỏ ra thật phiền toái. Đại loại như tự động đặt Bullet, tự động xuống dòng, tự động thêm dấu cách…

Tuy nhiên, khi thiết kế phần mềm hẳn là nhà sản xuất đã có dụng ý, nghiên cứu kỹ nhu cầu người dùng để đưa ra chúng. Vậy tại sao chúng ta không nghĩ sẽ làm chủ tính năng tự động đó để phục vụ mình một cách tối ưu.

Bài viết sau sẽ trình bày một số thủ thuật để tự động hóa quá trình định dạng văn bản trong MS Word 2013. Sẽ hoàn toàn tương tự cho các phiên bản khác.

1. <b>Thiết lập lại một số mặc định cơ bản</b>

<b>1.1. Thiết lập trang</b>

<b>File/ Print/ Page Setup </b>hoặc nhấp đôi vào <b>thanh Ruler</b> để hiển thị hộp thoại Page Setup. 

Đặt các thông số cần thiết: Lề và gáy đặt ở Tab Margin; khổ giấy A4 ở Tab Paper. 

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjX_Ao5xbyKQ4m2X4XkOahNM6m31Gxe5yCDliR_kp90OmqN7NPNYxcSZND66anlrC4CFLTuemoafl1-lv9CJNBenEGdrgpoWLy5VPmoUjHty_sHgkbcYcjG291eHnjPrVv9XN3i3LZEFx8/s1600/Picture1.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjX_Ao5xbyKQ4m2X4XkOahNM6m31Gxe5yCDliR_kp90OmqN7NPNYxcSZND66anlrC4CFLTuemoafl1-lv9CJNBenEGdrgpoWLy5VPmoUjHty_sHgkbcYcjG291eHnjPrVv9XN3i3LZEFx8/s1600/Picture1.png" width="640" height="368"></a>

Lưu ý: Nút <b>Set As Default</b> ở góc trái cuối hộp thoại cho phép mặc định lại các thông số đã đặt cho những file sau này, nếu các thông số sử dụng thường xuyên các bạn có thể nhấn nút này.<br>
<b>1.2. Thiết lập font chữ mặc định</b><br>

Truy cập Tab<b> Design/ Font/ Customize Font... </b>xuất hiện hộp thoại bên dưới, chọn font chữ bạn cần (thường chúng ta sử dụng Time New Roman, ở đây có 2 ô để mặc định cho tiêu đề và cho nội dung); đặt tên cho định dạng mới này; kích nút <b>Save</b> để lưu lại.

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjmfsKLiS1pV6FZ7WYXiVQ9UOnk5juLhg1FQzc60hHBMvPOa8ZKxJHZcdN8pi8RF3Vh_ASnbhjqHeUxsmSIq7KoeEf-WXj1ewezXHFAAOyPd8aN1yTtLKVQ1KGqK1IPCgyX7LoOK5G_e2g/s1600/Picture2.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjmfsKLiS1pV6FZ7WYXiVQ9UOnk5juLhg1FQzc60hHBMvPOa8ZKxJHZcdN8pi8RF3Vh_ASnbhjqHeUxsmSIq7KoeEf-WXj1ewezXHFAAOyPd8aN1yTtLKVQ1KGqK1IPCgyX7LoOK5G_e2g/s1600/Picture2.png" width="640" height="364"></a>

<b>1.3. Làm chủ các định dạng mẫu</b>

1.3.1. Tiêu đề

Giả sử chúng ta có bố cục bài báo cáo với yêu cầu như sau:

1. TIÊU ĐỀ CẤP 1               : cỡ 16, kiểu hoa, in đậm

1.1. TIÊU ĐỀ CẤP 2            : cỡ 14, kiểu hoa và đậm

1.1.1.Tiêu đề cấp 3              : cỡ 14, kiểu thường và đậm

1.1.1.1.Tiêu đề cấp 4           : cỡ 14, kiểu thường

Đặt con trỏ chuột tại dòng Tiêu đề 1, chọn Numbering với thể loại như hình sau. Tương tự cho tiêu đề cấp 2, 3, 4. Để <b>lùi cấp cho tiêu đề</b>, kích chuột vào Numbering của tiêu đề vừa tạo, nhấn phím <b>Tab</b>.

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgceyqg76dh6mZ6G-qZ8wM7pwAMztiR2AlXQUf3jxcJMFh1dOhV9UEayokZUlaQL4jZKxfoNkHIseMt1d52UMRgs_Ipu7AP4sLiCyMDk_rlQxtK1jaRwCzsPDu_Q7wxMOwQdS_y8Gie0y8/s1600/Picture3.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgceyqg76dh6mZ6G-qZ8wM7pwAMztiR2AlXQUf3jxcJMFh1dOhV9UEayokZUlaQL4jZKxfoNkHIseMt1d52UMRgs_Ipu7AP4sLiCyMDk_rlQxtK1jaRwCzsPDu_Q7wxMOwQdS_y8Gie0y8/s1600/Picture3.png" width="640" height="248"></a>

Chìa khóa: MS Word mặc định đằng sau Numbering hay Bullet là một ký tự Tab, do vậy khoảng cách này khá dài và thay đổi bất thường tùy vào chuỗi ký tự theo sau. Cách loại bỏ như sau.

<table><tbody>
<tr><td><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhzT1ESejktyoByjc6BaBmYkerp4Ry28IBJastaAmVdc1Ur8xkWnijzgVXynXgQbtt1Rw2eXUtdFE_ZRpjiPcgclyf0ZkuKJQgk_H66eK4mu1tiDeQtff011EhVVl22-mwmbggsSkScoq0/s1600/Picture5.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhzT1ESejktyoByjc6BaBmYkerp4Ry28IBJastaAmVdc1Ur8xkWnijzgVXynXgQbtt1Rw2eXUtdFE_ZRpjiPcgclyf0ZkuKJQgk_H66eK4mu1tiDeQtff011EhVVl22-mwmbggsSkScoq0/s1600/Picture5.png" width="640" height="380"></a></td></tr>
<tr><td>Đặt lại cách lề cho tiêu đề tùy mục đích của bạn, mình đặt lại 0 cm. <br>
Kích <b>Set for All Levels</b> nếu muốn áp dụng tất cả các cấp.</td></tr>
</tbody></table>

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtCw0VFnPADkUDjCc3VkSeQ8wASJK-kECKrw_26HGCmt2MK2lZmMkeIFAt9pEoGplk-IPMZk4QCzauJaDqQwePlnw-LrIhcYLzce0ppKKHnwm8bw8HtFPE1CidlmTLCRK7FdzLYSXF5Lk/s1600/Picture6.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtCw0VFnPADkUDjCc3VkSeQ8wASJK-kECKrw_26HGCmt2MK2lZmMkeIFAt9pEoGplk-IPMZk4QCzauJaDqQwePlnw-LrIhcYLzce0ppKKHnwm8bw8HtFPE1CidlmTLCRK7FdzLYSXF5Lk/s1600/Picture6.png"></a>

Kích nút <b>More/Less</b> ở góc trái dưới cùng hộp thoại, bạn sẽ thấy phần mở rộng. Chuyển thuộc tính <b>Follow number with:</b> thành <b>Space </b>(1 dấu cách theo sau Number).

Sau khi hoàn thành, các bạn tiếp tục định dạng cỡ chữ, màu chữ, font chữ cho tiêu đề nếu cần. Bước tiếp theo là lưu lại mẫu tiêu đề để áp dụng cho các tiêu đề khác. Quá trình được mô tả như sau:

<table><tbody>
<tr><td>
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiqZIOlx_5BaeBdqKpFr99uncUf61b_48iE9WN9xOtg4TpMbKiXjy6fChGfwxR-cIoni0-FROHldO88COWhCj9ZWpp1EZUb2jnAiNNJ_Ui1ysCucKC4oGyoPMxTYK2oNLbYI0Rj-XBOPik/s1600/Picture9.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiqZIOlx_5BaeBdqKpFr99uncUf61b_48iE9WN9xOtg4TpMbKiXjy6fChGfwxR-cIoni0-FROHldO88COWhCj9ZWpp1EZUb2jnAiNNJ_Ui1ysCucKC4oGyoPMxTYK2oNLbYI0Rj-XBOPik/s1600/Picture9.png" width="640" height="214"></a>

</td></tr>
<tr><td>Chọn tiêu cấp 1 đã định dạng, kích chuột phải vào <b>Heading 1 </b>trên thanh công cụ, chọn <b>Update Heading 1... </b>để lưu lại thuộc tính đã định dạng.</td></tr>
</tbody></table>
<table><tbody>
<tr><td><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh4tcUWu7Zq531ZoKrKTWv3lvid1dnwNqbaYZFCyhyeuRuK7T3evZN9ykzVs3mazl07HgASs324bQHtO-I2039oIS3tAgR9_vEgdm4OLekuL3IfnbGE2DXdShu6N0SraRTs9wEVDwOSYMs/s1600/Picture10.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh4tcUWu7Zq531ZoKrKTWv3lvid1dnwNqbaYZFCyhyeuRuK7T3evZN9ykzVs3mazl07HgASs324bQHtO-I2039oIS3tAgR9_vEgdm4OLekuL3IfnbGE2DXdShu6N0SraRTs9wEVDwOSYMs/s1600/Picture10.png" width="640" height="210"></a></td></tr>
<tr><td>Di chuyển đến 1 tiêu đề khác cùng cấp kích <b>Heading 1</b> để áp dụng định dạng đã lưu. Làm tương tự cho <b>Heading 2, 3, 4</b>...<br>

[Còn nữa]

</td></tr>
</tbody></table>
