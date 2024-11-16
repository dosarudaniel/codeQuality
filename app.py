from flask import Flask, request, jsonify, render_template
import subprocess
import csv, os

java_tmp_file = "Main.java"

app = Flask(__name__)

# Used to assign an unique username for a submission
def increment_student_string(student_string):
    # Check if the student name is "referinta"
    if student_string == "referinta":
        return 'student_1'
    
    # Split the string at the underscore to separate 'student' and the number
    prefix, number = student_string.split('_')
    
    # Convert the number part to an integer and increment it
    incremented_number = int(number) + 1
    
    # Reassemble the string with the incremented number
    new_student_string = f"{prefix}_{incremented_number}"
    
    return new_student_string

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runJar', methods=['POST'])
def run_jar():
    data = request.get_json()
    code = data.get('code')

    print(f"Received code: {code[0:15]}")
    response = {}

    # Compile the code
    try:
        # Step 1: Save the received code to a .java file
        with open(java_tmp_file, 'w', encoding='utf-8') as java_file:
            java_file.write(code)

        # Step 2: Compile the Java code using javac
        compile_result = subprocess.run(
            ['javac', java_tmp_file],     # Command to compile the file
            capture_output=True,        # Capture the output (both stdout and stderr)
            text=True                   # Return output as string
        )

        # Step 3: Check the compilation status
        if compile_result.returncode == 0:
            # Compilation successful
            response['message'] = "Compilation successful!"
            response['compiled'] = "True"
            print(f"{response['message']}")
        else:
            # Compilation failed, return error message
            response["message"] = "Compilation failed."
            response["compiled"] = False
            response["errors"] = compile_result.stderr  # Adding the errors in case of failure
            
            print(f"{response['message']}")
            return response

    except Exception as e:
        return jsonify({"message": "An error occurred.", "error": str(e)})
    

    
    print(f"Adding a new row in responses.csv")

    csv_file_path = ''
    # File path to the CSV file
    if os.name == 'nt':  # Windows
        csv_file_path = os.path.join('resources', 'input', 'responses.csv')
    else:  # Linux and other OS
        csv_file_path = 'resources/input/responses.csv'

    print(f"File path: {csv_file_path}")


    last_row = None
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            print(f"Reading responses csv file")
            next(reader)  # Skip the header row
            for row in reader: 
                if row[0] != '':
                    #print(f"{row[0]}, {row[1]}")
                    last_row = row

            
    except FileNotFoundError:
        # If the file doesn't exist, set last_row to None
        print(f"Cannot find file {csv_file_path}. Set last_row to None ")
        last_row = None
    except Exception as e:
        print(f"error while reading last row: {str(e)}")
        return jsonify({'error': str(e)}), 500
    

     # If there was a last row, extract data from it
    if last_row:
        print(f"Last row {last_row[0], last_row[1], last_row[2]}")
        student_id = str(int(last_row[0]) + 1)
        student_username = increment_student_string(last_row[1])
        challenge = last_row[2]
        score = '?'
        # Optional: Get the code from the last row (last_row[4]) if needed
    else:
        student_id = 1
        student_username = 'student_1'
        challenge = 'ECTEL_demo'
        score = '60'

    # Append the new entry to the CSV file
    new_row = [student_id, student_username, challenge, score, code]
    print(f"New row: {new_row[0]} {new_row[1]} {new_row[2]}")

    try:
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)

            file.flush()    # Ensure the internal Python buffer is flushed
            os.fsync(file.fileno()) 
            
            print(f"New row written: {new_row[0]} {new_row[1]} {new_row[2]}")
    except Exception as e:
        print(f"error while adding a new row {str(e)}")
        return jsonify({'error': str(e)}), 500

    jar_path = 'PmdSimple-main.jar'  # Hardcoded path to the .jar file
    try:
        result = subprocess.run(['java', '-jar', jar_path], capture_output=True, text=True)
        output = result.stdout
        print(f"output {output}")
        jsonify({'output': output})
    except Exception as e:
        print(f"error while running jar file {str(e)}")


    csv_output_file_path = ''

    if os.name == 'nt':  # Windows
        csv_output_file_path = os.path.join('resources', 'output', 'output.csv')
    else:  # Linux or other OS
        csv_output_file_path = os.path.join('resources', 'output', 'output.csv')

    print(f"CSV Output File Path: {csv_output_file_path}")

    code_quality_metrics = None
    try:
        with open(csv_output_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            print(f"Reading output csv file")
            next(reader)  # Skip the header row
            for row in reader: 
                if row[1] == student_username:
                    code_quality_metrics = row
                    break
    
        print(f"Code quality metrics: {code_quality_metrics}")
            
    except FileNotFoundError:
        # If the file doesn't exist, set code_quality_metrics to None
        print(f"Cannot find file {csv_output_file_path}. Set code_quality_metrics to None ")
        code_quality_metrics = None
    except Exception as e:
        print(f"error while reading code_quality_metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500
    # code_quality_metrics = jsonify({'code_quality_metrics': code_quality_metrics})
    response['code_quality'] = code_quality_metrics
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)
