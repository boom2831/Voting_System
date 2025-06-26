document.getElementById("proceedBtn").onclick = function() {
    document.getElementById("loginModal").style.display = "block";
}

window.onclick = function(event) {
    const modal = document.getElementById("loginModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.getElementById("voterBtn").addEventListener("click", function() {
    window.location.href = "voterlogin.html";
});

document.getElementById("adminBtn").addEventListener("click", function() {
    window.location.href = "adminlogin.html";
});

document.getElementById("checkResultsBtn").addEventListener("click", function() {
    window.location.href = "result.html";
});

document.getElementById('adminLoginForm').addEventListener('submit', function(event) {
    event.preventDefault();
});