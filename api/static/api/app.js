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
    }
}
