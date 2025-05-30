// 토큰 관리 함수
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

// API 요청 헬퍼 함수
async function fetchAPI(url, method = 'GET', data = null) {
    // options 변수 정의
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    // 인증 토큰이 있다면 헤더에 추가
    const token = getToken();
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // POST, PUT 요청인 경우 데이터를 JSON으로 변환하여 body에 추가
    if (data !== null && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        // 인증 오류 처리
        if (response.status === 401) {
            removeToken();
            window.location.href = '/login';
            return;
        }
        
        // 응답이 비어있는 경우(204 No Content) 또는 DELETE 요청인 경우 null 반환
        if (response.status === 204 || (method === 'DELETE' && response.ok)) {
            return null;
        }
        
        // 응답 내용 확인
        const contentType = response.headers.get('content-type');
        let result;
        
        if (contentType && contentType.includes('application/json')) {
            try {
                result = await response.json();
            } catch (e) {
                console.error('JSON 파싱 오류:', e);
                throw new Error('서버에서 올바른 JSON 응답을 반환하지 않았습니다.');
            }
        } else {
            // JSON이 아닌 경우 텍스트로 처리
            result = await response.text();
            console.log('서버 응답(텍스트):', result);
            
            if (!response.ok) {
                throw new Error(result || `서버 오류: ${response.status}`);
            }
            
            return result;
        }
        
        if (!response.ok) {
            throw new Error(result.detail || '요청 처리 중 오류가 발생했습니다.');
        }
        
        return result;
    } catch (error) {
        console.error('API 요청 오류:', error);
        throw error;
    }
}

// 페이지 로드 시 사용자 인증 상태 확인
document.addEventListener('DOMContentLoaded', function() {
    const token = getToken();
    const authNavItems = document.querySelectorAll('.auth-nav-item');
    const nonAuthNavItems = document.querySelectorAll('.non-auth-nav-item');
    
    if (token) {
        // 인증된 사용자용 메뉴 표시
        authNavItems.forEach(item => item.style.display = 'block');
        nonAuthNavItems.forEach(item => item.style.display = 'none');
        
        // 사용자 정보 가져오기
        if (typeof fetchUserInfo === 'function') {
            fetchUserInfo();
        }
    } else {
        // 비인증 사용자용 메뉴 표시
        authNavItems.forEach(item => item.style.display = 'none');
        nonAuthNavItems.forEach(item => item.style.display = 'block');
        
        // 현재 경로가 인증이 필요한 페이지인지 확인
        const authRequiredPaths = ['/dashboard', '/goals'];
        const currentPath = window.location.pathname;
        
        if (authRequiredPaths.some(path => currentPath.startsWith(path))) {
            window.location.href = '/login';
        }
    }
});

// 로그아웃 함수
function logout() {
    removeToken();
    window.location.href = '/';
}

// 링크에 로그아웃 이벤트 연결
document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
});

// API 요청 상태 관리를 위한 헬퍼 함수
function setLoading(elementId, isLoading, loadingText = '로딩 중...') {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const originalText = element.getAttribute('data-original-text') || element.innerHTML;
    
    if (isLoading) {
        // 원래 텍스트 저장
        element.setAttribute('data-original-text', originalText);
        element.disabled = true;
        element.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${loadingText}`;
    } else {
        // 원래 텍스트로 복원
        element.disabled = false;
        element.innerHTML = originalText;
    }
}

// 에러 메시지 표시 함수
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.innerHTML = `<div class="alert alert-danger">${message}</div>`;
}

// 성공 메시지 표시 함수
function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.innerHTML = `<div class="alert alert-success">${message}</div>`;
}