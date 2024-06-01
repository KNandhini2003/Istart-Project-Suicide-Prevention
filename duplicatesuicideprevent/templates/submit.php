<?php
// Establish connection to MySQL
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "sprevent"; // Changed to 'sprevent' as per your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Assuming you're receiving the data from a form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Escape user inputs to prevent SQL injection
    $q1_value = isset($_POST['q1']) ? $_POST['q1'] : ''; // Value of q1
    $q2_value = isset($_POST['q2']) ? $_POST['q2'] : ''; // Value of q2
    $q3_value = isset($_POST['q3']) ? $_POST['q3'] : ''; // Value of q3
    $q4_value = isset($_POST['q4']) ? $_POST['q4'] : ''; // Value of q4
    $q5_value = isset($_POST['q5']) ? $_POST['q5'] : ''; // Value of q5
    $q6_value = isset($_POST['q6']) ? $_POST['q6'] : ''; // Value of q6
    $q7_value = isset($_POST['q7']) ? $_POST['q7'] : ''; // Value of q7
    $q8_value = isset($_POST['q8']) ? $_POST['q8'] : ''; // Value of q8
    $q9_value = isset($_POST['q9']) ? $_POST['q9'] : ''; // Value of q9
    $q10_value = isset($_POST['q10']) ? $_POST['q10'] : ''; // Value of q10

    // Calculate total value
    $total_value = $q1_value + $q2_value + $q3_value + $q4_value + $q5_value + $q6_value + $q7_value + $q8_value + $q9_value + $q10_value;

    // Determine risk level based on total value
    if ($total_value >= 0 && $total_value <= 13) {
        $risk_level = "Low";
    } elseif ($total_value >= 14 && $total_value <= 26) {
        $risk_level = "Medium";
    } elseif ($total_value >= 27 && $total_value <= 40) {
        $risk_level = "High";
    } else {
        $risk_level = "Unknown";
    }

    // Insert values into the database
    $sql = "INSERT INTO prevent (q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, total_value, risk_level) VALUES ('$q1_value', '$q2_value', '$q3_value', '$q4_value', '$q5_value', '$q6_value', '$q7_value', '$q8_value', '$q9_value', '$q10_value', '$total_value', '$risk_level')";

    if ($conn->query($sql) === TRUE) {
        echo "Record inserted successfully! Risk Level: " . $risk_level;
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    // Close the database connection
    $conn->close();
}
?>
