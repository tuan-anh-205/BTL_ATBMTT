GIỚI THIỆU BÀI TOÁN
    Trong thời đại số hóa, việc bảo vệ dữ liệu cá nhân đang trở nên vô cùng quan trọng. Các thông tin nhạy cảm như số căn cước công dân (CCCD), mã số bảo hiểm xã hội (BHXH), hay số tài khoản ngân hàng nếu bị lộ có  thể gây hậu quả nghiêm trọng cho người dùng. Do đó, việc áp dụng các kỹ thuật mã hóa dữ liệu trước khi lưu trữ là cần thiết để đảm bảo tính bảo mật và an toàn thông tin.
    Trong đồ án này, chúng em xây dựng một ứng dụng web quản lý người dùng với cơ chế bảo mật dữ liệu sử dụng các thuật toán mã hóa hiện đại:
    Số CCCD được mã hóa bằng thuật toán Triple DES (3DES).
    Thông tin số BHXH và số tài khoản ngân hàng được mã hóa bằng thuật toán AES-256.
    Hệ thống sử dụng cặp khóa riêng cho từng người dùng và không lưu trữ dữ liệu gốc ở dạng văn bản thuần trong cơ sở dữ liệu.
+ Giới thiệu thuật toán Triple DES và AES
- Triple DES (3DES)
    Triple DES là một thuật toán mã hóa đối xứng được phát triển từ thuật toán DES (Data Encryption Standard). Trong 3DES, dữ liệu được mã hóa ba lần với ba khóa 56-bit khác nhau, theo thứ tự: mã hóa → giải mã → mã hóa. Điều này giúp tăng độ an toàn so với DES ban đầu.
    Trong hệ thống của chúng em, 3DES được sử dụng để mã hóa số CCCD vì kích thước nhỏ, phù hợp với việc xử lý nhanh, và vẫn đảm bảo an toàn khi dùng trong quy mô ứng dụng nhỏ.
- AES (Advanced Encryption Standard)
    AES là thuật toán mã hóa đối xứng được tiêu chuẩn hóa bởi NIST (Hoa Kỳ) với ba mức độ bảo mật: AES-128, AES-192 và AES-256. Trong đó, AES-256 cung cấp mức bảo mật cao nhất với khóa dài 256 bit.
    AES có tốc độ mã hóa nhanh, mức độ an toàn cao và được sử dụng phổ biến trong thực tế (ví dụ: HTTPS, VPN, dữ liệu tài chính). Trong đồ án này, AES-256 được dùng để mã hóa thông tin BHXH và số tài khoản ngân hàng – vốn là những trường dữ liệu có độ nhạy cảm cao hơn.
+ Chức năng chính của hệ thống
- Người dùng có thể:
    Đăng ký tài khoản, đăng nhập
    Xem, chỉnh sửa thông tin cá nhân
    Đổi mật khẩu
    Xóa tài khoản của chính mình
    Quản trị viên có thể:
    Xem danh sách người dùng (dưới dạng đã mã hóa)
    Nhập mật khẩu xác minh để giải mã thông tin người dùng
    Sửa, xóa thông tin người dùng
    Đổi mật khẩu cho người dùng khác
    Ghi log mỗi thao tác xem, sửa, xóa để theo dõi lịch sử hệ thống
Kết luận
    Hệ thống ứng dụng mã hóa dữ liệu với DES và AES cho thấy khả năng bảo vệ thông tin người dùng khỏi các mối đe dọa từ truy cập trái phép hoặc rò rỉ cơ sở dữ liệu. Với việc phân quyền rõ ràng và ghi log đầy đủ, ứng dụng mô phỏng một hệ thống bảo mật đơn giản nhưng có tính thực tế, giúp sinh viên tiếp cận gần hơn với các nguyên lý của bảo mật thông tin trong đời sống và công nghệ.
