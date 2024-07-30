// document.addEventListener('DOMContentLoaded', function(){
//     // Get references to the fixed fields
//     const fixedField1 = document.getElementById('City');

//     // Add event listeners to the fixed fields
//     fixedField1.addEventListener('blur', autoFillFields);

//     function autoFillFields(){
//         // Get references to the fields to be auto-filled
//         const autoField1 = document.getElementById('State');
//         const autoField2 = document.getElementById('Pin');
//         const autoField3 = document.getElementById('Country-of-Origin');

//         // Check if both fixed fields are filled
//         if (fixedField1.value) {
//             if(fixedField1.value == "Ahemdabad")
//             {
//                 autoField1.value = 'Gujarat';
//                 autoField2.value = '380015'
//                 autoField3.value = 'India';
//             }
//             else if(fixedField1.value == "Kanpur")
//             {
//                 autoField1.value = 'UP';
//                 autoField2.value = '208001'
//                 autoField3.value = 'Bharat';
//             }
//             else
//             {
//                 autoField1.value = "Information doesn't exist corresponding to this credentials";
//                 autoField2.value = "Information doesn't exist corresponding to this credentials";
//             }
//             // Auto-fill the other fields based on the values of the fixed fields
//             // autoField1.value = fixedField1.value + ' - auto filled';
//             // autoField2.value = fixedField2.value + ' - auto filled';
//         }else{
//             // Clear the auto-filled fields if the fixed fields are not both filled
//             autoField1.value = '';
//             autoField2.value = '';
//         }
//     }
// });
