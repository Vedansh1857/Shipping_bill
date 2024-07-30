document.addEventListener('DOMContentLoaded', function(){
    // Get references to the fixed fields
    const fixedField1 = document.getElementById('City');

    // Add event listeners to the fixed fields
    fixedField1.addEventListener('blur', autoFillFields);

    function autoFillFields(){
        // Get references to the fields to be auto-filled
        const autoField1 = document.getElementById('State');
        const autoField2 = document.getElementById('Pin');
        const autoField3 = document.getElementById('Branch-Sr-No.');

        // Check if both fixed fields are filled
        if (fixedField1.value) {
            if(fixedField1.value == "12345")
            {
                autoField1.value = 'Vedansh';
                autoField2.value = 'a1b2c3'
                autoField3.value = '1';
            }
            else if(fixedField1.value == "67890")
            {
                autoField1.value = 'Anurag';
                autoField2.value = 'd4e5f6'
                autoField3.value = '2';
            }
            else
            {
                autoField1.value = "Information doesn't exist corresponding to this credentials";
                autoField2.value = "Information doesn't exist corresponding to this credentials";
            }
            // Auto-fill the other fields based on the values of the fixed fields
            // autoField1.value = fixedField1.value + ' - auto filled';
            // autoField2.value = fixedField2.value + ' - auto filled';
        }else{
            // Clear the auto-filled fields if the fixed fields are not both filled
            autoField1.value = '';
            autoField2.value = '';
        }
    }
});
