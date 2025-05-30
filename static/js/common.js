// 사용자 정보 로드 함수
async function loadUserInfo() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/login';
            return;
        }

        const response = await fetch('/api/users/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('사용자 정보를 가져오지 못했습니다.');
        }

        const userData = await response.json();

        // 사용자 이름 표시
        const userNameElement = document.getElementById('user-name');
        if (userNameElement) {
            userNameElement.textContent = userData.username;
        }
    } catch (error) {
        console.error('사용자 정보 로드 오류:', error);
    }
}

// 로그아웃 기능
function setupLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            localStorage.removeItem('token');
            window.location.href = '/login';
        });
    }
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function () {
    loadUserInfo();
    setupLogout();
});