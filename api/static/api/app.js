function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function addDynamicRow() {
    var dynamicFieldName = $("#dynamic-field-name")[0].value;
    var dynamicFieldType = $("#dynamic-field-type")[0].value;

    dynamicFieldName = dynamicFieldName.trim().split(" ")
    var cDynamicFieldName = "";
    for (let i = 0; i < dynamicFieldName.length; i++) {
        if (dynamicFieldName[i]) {
            cDynamicFieldName = cDynamicFieldName.concat(' ', capitalizeFirstLetter(dynamicFieldName[i]));
        }
    }
    cDynamicFieldName = cDynamicFieldName.trim();
    var alreadyAdded = $(`[id='p-` + cDynamicFieldName + `']`);
    if (cDynamicFieldName !== "" && alreadyAdded.length === 0) {
        var dynamicField = $(`<div class="u-s-m-b-30"><label class="gl-label" for="p-` + cDynamicFieldName + `">` + cDynamicFieldName + `</label><input class="input-text input-text--primary-style" type="` + dynamicFieldType + `" name="p-` + cDynamicFieldName + `"id="p-` + cDynamicFieldName + `" placeholder="Enter ` + cDynamicFieldName + `" /></div>`);
        $("#dynamic-field-text").before(dynamicField);
        $("#dynamic-field-name")[0].value = "";
    }
}

function addLessonRow() {
    var lessonAddButton = $("#lesson-add-button")[0];
    var id = 0;
    while (true) {
        id++;
        var lastLesson = $("#p-Lessons-" + id);
        if (lastLesson.length === 0) {
            break
        }
    }
    var newLessonRow = $(`<input class="input-text input-text--primary-style u-s-m-l-6" type="text" name="p-Lessons-` + id + `" id="p-Lessons-` + id + `" placeholder="Enter Lesson Name"/>`);
    lessonAddButton.before(newLessonRow[0]);
}

function addCameraRow() {
    var cameraAddButton = $("#camera-add-button");
    var cameraFieldName = $("#camera-field-name")[0].value;
    cameraFieldName = cameraFieldName.trim().split(" ")
    var cCameraFieldName = "";
    for (let i = 0; i < cameraFieldName.length; i++) {
        if (cameraFieldName[i]) {
            cCameraFieldName = cCameraFieldName.concat(' ', capitalizeFirstLetter(cameraFieldName[i]));
        }
    }
    cCameraFieldName = cCameraFieldName.trim();
    console.log(cCameraFieldName);
    var alreadyAdded = $(`[id='p-Camera.` + cCameraFieldName + `']`);
    if (cCameraFieldName !== "" && alreadyAdded.length === 0) {
        var dynamicField = $(`<div class="u-s-m-b-30"><label class="gl-label" for="p-Camera-` + cCameraFieldName + `">` + cCameraFieldName + `</label><input class="input-text input-text--primary-style" type="text" name="p-Camera-` + cCameraFieldName + `"id="p-Camera-` + cCameraFieldName + `" placeholder="Enter ` + cCameraFieldName + `" /></div>`);
        $("#camera-field-div").before(dynamicField);
        $("#camera-field-name")[0].value = "";
    }
}

function changeProductTab(clicked_id) {
    var descTabButton = $("#pd-desc-tab")[0];
    var descField = $("#pd-desc")[0];
    var contactTabButton = $("#pd-contact-tab")[0];
    var contactField = $("#pd-contact")[0];
    if (clicked_id === "pd-contact-tab") {
        descTabButton.classList.remove('active');
        contactTabButton.classList.add('active');

        descField.classList.remove('active');
        contactField.classList.add('active');
        contactField.classList.add('show');
    } else {
        descTabButton.classList.add('active');
        contactTabButton.classList.remove('active');

        descField.classList.add('active');
        descField.classList.add('show');
        contactField.classList.remove('active');
    }
}
