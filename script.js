document.addEventListener('DOMContentLoaded', function(){
    // Get references to the fixed fields
    const fixedField1 = document.getElementById('Item_Description_1');

    // Add event listeners to the fixed fields
    fixedField1.addEventListener('blur', autoFillFields);

    function autoFillFields(){
        // Get references to the fields to be auto-filled
        const autoField1 = document.getElementById('Unit_Price');
        const autoField2 = document.getElementById('Unit_of_rate');
        const autoField3 = document.getElementById('Unit_of_Measurement1');

        // Check if both fixed fields are filled
        if (fixedField1.value) {
            if(fixedField1.value == "Item_Description_1: Turmeric powder")
                {
                    autoField1.value = '10';
                    autoField2.value = 'USD';
                    autoField3.value = 'USDollars';
                }
            else if(fixedField1.value == "Item_Description_1: Wooden mandir")
            {
                autoField1.value = '20';
                autoField2.value = 'INR';
                autoField3.value = 'IndianRupee';
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
