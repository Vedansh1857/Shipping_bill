document.addEventListener('DOMContentLoaded', function(){
    // Get references to the fixed fields
    const fixedField1 = document.getElementById('Name-of-the-Importer');

    // Add event listeners to the fixed fields
    fixedField1.addEventListener('blur', autoFillFields);

    function autoFillFields(){
        // Get references to the fields to be auto-filled
        const autoField1 = document.getElementById('Adress1');
        const autoField2 = document.getElementById('City');
        const autoField3 = document.getElementById('Pin');

        // Check if both fixed fields are filled
        if (fixedField1.value) {
            if(fixedField1.value == "David Import USA")
                {
                    autoField1.value = '2345 wall street';
                    autoField2.value = 'New York';
                    autoField3.value = '73844474';
                }
            else if(fixedField1.value == "Vedansh")
            {
                autoField1.value = 'Daulatganj';
                autoField2.value = 'Kanpur';
                autoField3.value = '208001';
            }
            else
            {
                autoField1.value = "Invalid credentials";
                autoField2.value = "Invalid credentials";
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
