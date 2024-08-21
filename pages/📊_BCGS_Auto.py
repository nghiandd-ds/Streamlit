import streamlit as st
from base import request_gpt

st.set_page_config(
    page_title="BCGS Auto", 
    page_icon="🤖",
)

st.write("# BCGS Auto 📊")
    
# upload file by streamlit
uploaded_file = st.file_uploader("Upload file")

if not uploaded_file:
    st.stop()


prompt = """
1.
Đây là ngưỡng tham chiếu đánh giá hiệu năng của mô hình A-score:
-	AR A-score lớn hơn hoặc bằng 35%: Xanh. Khả năng phân biệt tốt
-	AR A-score lớn hơn hoặc bằng 25% và nhỏ hơn 35%: Vàng. Có thể chấp nhận
-	AR A-score nhỏ hơn 25%: Đỏ. Nằm ngoài khoảng chấp nhận

Đây là ví dụ về việc viết kết luận đánh giá hiệu năng giai đoạn giám sát mô hình các mô hình A-score:
-	Mô hình PD R:
+ Giai đoạn phát triển mô hình: 36.18%
+ Giai đoạn giám sát mô hình: 
•	Loại bỏ các quan sát indeterminate: 29.59%
•	Bao gồm các quan sát indeterminate: 29.35%
-	Mô hình PD I:
+ Giai đoạn phát triển mô hình: 43.46%
+ Giai đoạn giám sát mô hình: 
•	Loại bỏ các quan sát indeterminate: 9.60%
•	Bao gồm các quan sát indeterminate: 9.50%
-	Mô hình PD E:
+ Giai đoạn phát triển mô hình: 37.20%
+ Giai đoạn giám sát mô hình: 
•	Loại bỏ các quan sát indeterminate: 26.03%
•	Bao gồm các quan sát indeterminate: 25.83%
-	Mô hình PD U:
+ Giai đoạn phát triển mô hình: 31.60%
+ Giai đoạn giám sát mô hình: 
•	Loại bỏ các quan sát indeterminate: 25.16%
•	Bao gồm các quan sát indeterminate: 24.44%

Kết luận: Đối với cấu phần A-score: khả năng phân biệt có sự sụt giảm so với giai đoạn xây dựng mô hình tuy nhiên giá trị AR A-score nằm trong/ xấp xỉ ngưỡng “Có thể chấp nhận” đối với các mô hình PD R, PD E, PD U (đối với cả 02 mẫu bao gồm/ không bao gồm indeterminate). Đối với mô hình PD I, giá trị AR A-score ở ngưỡng “Nằm ngoài khoảng chấp nhận” đối với cả 02 mẫu (bao gồm/ không bao gồm indeterminate).

2.
Đây là ngưỡng tham chiếu đánh giá hiệu năng của mô hình B-score:
-	AR B-score lớn hơn hoặc bằng 55%: Xanh. Khả năng phân biệt tốt
-	AR B-score lớn hơn hoặc bằng 40% và nhỏ hơn 55%: Vàng. Có thể chấp nhận
-	AR B-score nhỏ hơn 40%: Đỏ. Nằm ngoài khoảng chấp nhận

Đây là ví dụ về việc viết kết luận đánh giá hiệu năng giai đoạn giám sát mô hình các mô hình B-score:
-	Mô hình PD R:
+ Giai đoạn phát triển mô hình: 82.04%
+ Giai đoạn giám sát mô hình:
•	Loại bỏ các quan sát indeterminate: 64.81%
•	Bao gồm các quan sát indeterminate: 63.99%
-	Mô hình PD I:
+ Giai đoạn phát triển mô hình: 77.27%
+ Giai đoạn giám sát mô hình: 
•	Loại bỏ các quan sát indeterminate: 67.83%
•	Bao gồm các quan sát indeterminate: 67.32%
-	Mô hình PD E:
+ Giai đoạn phát triển mô hình: 74.00%
+ Giai đoạn giám sát mô hình: 
•	Loại bỏ các quan sát indeterminate: 64.16%
•	Bao gồm các quan sát indeterminate: 63.33%
-	Mô hình PD U:
+ Giai đoạn phát triển mô hình: 68.20%
+ Giai đoạn giám sát mô hình: 
•	Loại bỏ các quan sát indeterminate: 69.08%
•	Bao gồm các quan sát indeterminate: 67.34%

Kết luận: Đối với cấu phần B-score: khả năng phân biệt có sự sụt giảm so với giai đoạn phát triển mô hình tuy nhiên giá trị AR B-score nằm trong ngưỡng “Khả năng phân biệt tốt” đối với các phân khúc PD R, PD I, PD E, PD U (đối với cả 02 mẫu bao gồm/ không bao gồm indeterminate).

Từ các ngưỡng tham chiếu và các ví dụ viết kết luận ở trên, hãy viết kết luận cho kết quả Giám sát mô hình ở bảng kết quả trong file sau, chỉ tập trung vào phần kết luận tổng kết, viết 1 câu kết luận cho mô hình A-score, 1 câu kết luận cho mô hình B-score.
"""

if st.button("Viết kết luận"):
    request_gpt(uploaded_file, prompt, "summary")






# Đây là ngưỡng tham chiếu đánh giá hiệu năng của mô hình Pooling:
# -	AR Pooling ≥ 50%: Xanh. Khả năng phân biệt tốt
# -	40% ≤ AR Pooling < 50%: Vàng. Có thể chấp nhận
# -	AR Pooling < 40%: Đỏ. Nằm ngoài khoảng chấp nhận

# Đây là bảng ngưỡng tham chiếu đánh giá Mức độ ổn định của mô hình;
# -	PSI ≤ 0.1: Xanh. Phân phối ổn định
# -	0.1 < AR ≤ 0.25: Vàng. Phân phối có sự dịch chuyển nhỏ
# -	AR > 0.25: Đỏ. Phân phối có sự dịch chuyển lớn

# Đây là ví dụ về việc viết kết luận đánh giá Mức độ ổn định của các mô hình:
# -	PD R: PSI = 0.167
# -	PD I: PSI = PSI cấu phần A-Score = 0.264 và PSI cấu phần B-Score = 0.0912
# -	PD T: PSI = 0.597
# -	PD E: PSI = 0.0241
# -	PD U: PSI = 0.0705

# Kết luận: Cấu phần phân nhóm Pooling của mô hình PD T có sự thay đối lớn trong phân phối, với kết quả chỉ số PSI nằm ở ngưỡng đỏ. Sự thay đổi trong phân phối và nguyên nhân đã được nhận thức và ghi nhận. Các mô hình khác có phân phối thay đổi không đáng kể, ngoại trừ cấu phần A-score của mô hình PD I có chỉ số PSI ở ngưỡng đỏ - tuy nhiên, cần lưu ý rằng cấu phần PD I A-score chứa các chỉ tiêu pilot từ chi nhánh và bộ mẫu phát triển (hiện đang làm cơ sở để thực hiện kiểm tra PSI) không bao phủ toàn bộ danh mục.

# Đây là ngưỡng đánh giá mức độ tập trung của mô hình:
# Mức độ tập trung của cấu phần phân nhóm Pooling được đo lường thông qua chỉ số mức độ tập trung của phân phối (Herfindahl-Hirschman Index - HHI). Theo thông lệ quốc tế, chỉ số này nhận giá trị từ 0.25 trở lên sẽ tương ứng với mức độ tập trung lớn của mô hình.

# Đây là ví dụ về việc viết kết luận đánh giá Mức độ tập trung của các mô hình:

# -	PD R: HHI tập phát triển = 0.1788. HHI tập giám sát = 0.1739
# -	PD I: HHI tập phát triển: Cấu phần A-score = 0.2266, cấu phần B-score = 0.2342. HHI tập giám sát: A-score = 0.2983, cấu phần B-score = 0.2366.
# -	PD T: HHI tập phát triển = 0.0884. HHI tập giám sát = 0.1596
# -	PD E: HHI tập phát triển = 0.3578. HHI tập giám sát = 0.3404
# -	PD U: HHI tập phát triển = 0.1845. HHI tập giám sát = 0.1894

# Kết luận: Tất cả các mô hình có mức độ tập trung tương đối nhất quán với kết quả xây dựng mô hình, ngoại trừ câu phần PD I A-score có HHI gia tăng ở ngưỡng đỏ - tuy nhiên, cần lưu ý rằng cấu phần PD I A-score chứa các chỉ tiêu pilot từ chi nhánh và bộ mẫu phát triển (hiện đang làm cơ sở để thực hiện kiểm tra HHI) không bao phủ toàn bộ danh mục.


# Đánh giá hiệu năng của các chỉ tiêu (biến) thuộc cấu phần A-score, B-score
# Tương tự như đánh giá hiệu năng cấp độ mô hình, chỉ số AR sẽ được sử dụng để đánh giá hiệu năng phân biệt của chỉ tiêu. Sụt giảm AR đáng kể được hiểu là sụt giảm từ 30% trở lên.
# -	PD R:
# + Cấu phần A-score:
# •	Tuổi của khách hàng: AR mẫu phát triển = 2,45%. AR mẫu giám sát = 1,04%.
# •	Loại cơ quan: AR mẫu phát triển = 21,45%. AR mẫu giám sát = 23,84%.
# •	Hình thức thanh toán lương và thu nhập khác: AR mẫu phát triển = 16,90%. AR mẫu giám sát = 21,27%.
# •	Tình trạng hôn nhân: AR mẫu phát triển = 3,85%. AR mẫu giám sát = 7,67%.
# •	Số người trực tiếp phụ thuộc vào kinh tế của người vay: AR mẫu phát triển = 8,20%. AR mẫu giám sát = -3,49%.
# •	Số năm làm việc trong lĩnh vực chuyên môn hiện tại: AR mẫu phát triển = 3,62%. AR mẫu giám sát = 6,40%.
# •	Số tiền xin vay/ (Thu nhập của khách hàng x Kỳ hạn của khoản vay): AR mẫu phát triển = 13,02%. AR mẫu giám sát = -4,91%.
# + Kết luận: Các chỉ tiêu có hiệu năng phân biệt sụt giảm không đáng kể / cải thiện so với giai đoạn xây dựng mô hình, ngoại trừ chỉ tiêu “Tuổi của khách hàng", “Số người trực tiếp phụ thuộc vào kinh tế của người vay” và “Số tiền xin vay/ Thu nhập của khách hàng x Kỳ hạn của khoản vay)”.
# + Cấu phần B-score: 
# •	Kỳ hạn của khoản vay (đơn vị: tháng): AR mẫu phát triển = 18,76%. AR mẫu giám sát = -0,88%.
# •	Khách hàng có tài khoản tiết kiệm tại thời điểm quan sát: AR mẫu phát triển = 2,35%. AR mẫu giám sát = 7,72%.
# •	Tuổi của khách hàng tại thời điểm quan sát: AR mẫu phát triển = 16,35%. AR mẫu giám sát = 9,70%.
# •	Một tài sản bảo đảm cho nhiều khoản vay: AR mẫu phát triển = 11,85%. AR mẫu giám sát = 1,95%.
# •	Trung bình số dư tài khoản thanh toán/ Trung bình dư nợ trong 6 tháng qua: AR mẫu phát triển = 40,88%. AR mẫu giám sát = 50,71%.
# •	Trung bình số tiền thực trả/ Trung bình số tiền phải trả trong vòng 6 tháng qua: AR mẫu phát triển = 46,33%. AR mẫu giám sát = 14,88%.
# •	Số lần quá hạn trong 6 tháng qua : AR mẫu phát triển = 65,41%. AR mẫu giám sát = 44,37%.
# + Kết luận: Một số chỉ tiêu có hiệu năng suy giảm đáng kể, tuy nhiên, mô hình vẫn đang sử dụng một số chỉ tiêu có khả năng phân biệt rất cao, bao gồm “Trung bình số dư tài khoản thanh toán/ Trung bình dư nợ trong 6 tháng qua”, “Số lần quá hạn trong 6 tháng qua”.


