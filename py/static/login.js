async function checkLogin(event) {
    event.preventDefault(); // Ngăn form submit mặc định

    let email = document.getElementById("email").value;
    let password = document.getElementById("pass").value;

    let response = await fetch("/check-login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ email, pass: password })
    });

    try {
        let data = await response.json();
        console.log(data);

        if (data.success) {
            alert("Đăng nhập thành công! Chào " + data.name);
            window.location.href = data.role === "admin" ? "/admin" : "/index-vi";
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error("Lỗi: Server không trả về JSON hợp lệ!", error);
    }
}

    function showForgotForm() {
            document.getElementById("formBlock").style.display = "none";
            document.getElementById("forgotPasswordForm").style.display = "block";
        }

        function sendEmailToAdmin() {
            let phone = document.getElementById("forgotPhone").value;
            let cccd = document.getElementById("forgotCCCD").value;

            if (!phone || !cccd) {
                alert("Vui lòng nhập đầy đủ thông tin!");
                return;
            }

            let adminEmail = "yukiyukine123@gmail.com";
            let subject = encodeURIComponent("Yêu cầu cấp lại mật khẩu");
            let body = encodeURIComponent(`Thông tin người yêu cầu:\n- SĐT: ${phone}\n- CCCD: ${cccd}`);

            let gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=${adminEmail}&su=${subject}&body=${body}`;
            
            let newTab = window.open(gmailLink, "_blank");

            if (!newTab) {
                alert("Trình duyệt có thể đang chặn cửa sổ bật lên. Hãy cho phép pop-up và thử lại!");
            } else {
                alert("Yêu cầu đã được gửi.");
                closeForm();
            }
        }

        function closeForm() {
            document.getElementById("forgotPasswordForm").style.display = "none";
            document.getElementById("formBlock").style.display = "block";
        }

        // Gán sự kiện bằng JavaScript thay vì dùng `onclick` trong HTML
        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById("sendRequestBtn").addEventListener("click", sendEmailToAdmin);
        });
        function startFaceLogin() {
            fetch("http://127.0.0.1:5000/face-login")
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        alert("Đăng nhập thành công!");
                        window.location.href = "index-vi.html"; // Chuyển hướng sau khi đăng nhập
                    } else {
                        alert("Không nhận diện được khuôn mặt.");
                    }
                })
                .catch(error => console.error("Lỗi:", error));
        }
        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById("formBlock").addEventListener("submit", checkLogin);
});

