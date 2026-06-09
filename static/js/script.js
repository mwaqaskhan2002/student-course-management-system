document.addEventListener("DOMContentLoaded", function () {
  // Saare alerts ko dhoondo
  const alerts = document.querySelectorAll(".alert");

  alerts.forEach(function (alert) {
    setTimeout(function () {
      // Check karein ke Bootstrap load ho chuka hai ya nahi
      if (typeof bootstrap !== "undefined") {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        if (bsAlert) {
          bsAlert.close();
        }
      } else {
        // Fallback: Agar bootstrap bundle load na bhi ho, toh normal HTML se hide kar do
        alert.style.display = "none";
      }
    }, 1500); // 1.5 seconds ka timer
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const departmentSelect = document.getElementById("id_department");
  const coursesContainer = document.querySelector("#id_courses"); // Django checkboxes wrapper

  if (departmentSelect && coursesContainer) {
    departmentSelect.addEventListener("change", function () {
      const departmentId = this.value;

      if (!departmentId) {
        coursesContainer.innerHTML =
          '<p class="text-muted small">Please select a department first.</p>';
        return;
      }

      // AJAX Request jo humne views mein banaya tha
      fetch(`/students/ajax/load-courses/?department_id=${departmentId}`)
        .then((response) => response.json())
        .then((data) => {
          coursesContainer.innerHTML = ""; // Purane checkboxes saaf karein

          if (data.length === 0) {
            coursesContainer.innerHTML =
              '<p class="text-danger small">No courses found for this department.</p>';
            return;
          }

          // Naye checkboxes create karein dynamic
          data.forEach((course) => {
            const div = document.createElement("div");
            div.className = "form-check mb-1";
            div.innerHTML = `
                            <input class="form-check-input" type="checkbox" name="courses" value="${course.id}" id="id_courses_${course.id}">
                            <label class="form-check-label" for="id_courses_${course.id}">
                                ${course.course_name} (${course.course_code})
                            </label>
                        `;
            coursesContainer.appendChild(div);
          });
        })
        .catch((error) => console.error("Error loading courses:", error));
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const departmentSelect = document.querySelector('select[name="department"]');
  const coursesContainer = document.querySelector(".card.p-3.bg-light .row");

  if (departmentSelect && coursesContainer) {
    departmentSelect.addEventListener("change", function () {
      const departmentId = this.value;

      // Django API ko hit karein bina page reload kiye
      fetch(
        `{% url 'students:ajax_get_courses' %}?department_id=${departmentId}`,
      )
        .then((response) => response.json())
        .then((data) => {
          coursesContainer.innerHTML = ""; // Purane checkboxes saaf karein

          if (data.courses.length === 0) {
            coursesContainer.innerHTML = `
                            <div class="col-12 text-muted small">
                                <i class="ri-information-line"></i> No courses available for this department.
                            </div>`;
            return;
          }

          // Naye filtered courses ke checkboxes generate karein
          data.courses.forEach((course) => {
            const checkboxHtml = `
                            <div class="col-md-6 mb-2">
                                <div class="form-check">
                                    <input type="checkbox" name="courses" value="${course.id}" class="form-check-input" id="id_courses_${course.id}">
                                    <label class="form-check-label ms-2 text-dark" for="id_courses_${course.id}">
                                        ${course.course_name} (${course.course_code})
                                    </label>
                                </div>
                            </div>`;
            coursesContainer.insertAdjacentHTML("beforeend", checkboxHtml);
          });
        })
        .catch((error) => console.error("Error fetching courses:", error));
    });
  }
});