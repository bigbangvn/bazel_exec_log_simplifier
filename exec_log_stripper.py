
# To investigate Bazel cache miss issue we need to parse execution log and compare to check which input changes
# Because the log file is usually very big (x0MB) and there're alot of files that we know they don't change (because we can see git log)
# So stripping all of them will make the log file much smaller and easier to investigate the cause of Bazel cache-miss issue

def stripInput(start_token, input_file, output_path, detector_func):
  inputFile = open(input_file, 'r') # Execution log need to be parsed already by bazel log parser https://docs.bazel.build/versions/main/remote-execution-caching-debug.html
  outputFile = open(output_path, 'w')

  extensions = [".swift", ".h", ".m", ".mm", ".sh", ".strings", ".a", ".o", ".png", ".nib", ".plist", ".json", ".pdf", ".car"]
  print("Stripping all inputs with extensions:")
  print(extensions)

  end_token = '}\n'

  lines = inputFile.readlines()
  waiting_end = False
  detected = False
  tempLines = []
  for line in lines:
    if line == start_token:
      waiting_end = True
    elif waiting_end:
      if line == end_token:
        if not detected:
          outputFile.writelines(start_token)
          outputFile.writelines(tempLines)
          outputFile.writelines(end_token)

        # Reset
        tempLines.clear()
        waiting_end = False
        detected = False
      else:
        if not detected:
          detected = detector_func(line)
          print(detected)
        tempLines.append(line)
    else:
      outputFile.writelines(line)
  
  inputFile.close()
  outputFile.close()
  return output_path

# Cache-miss of an action is caused by changes inputs, so we trip all outputs to reduce log size
def stripAllOutput(input_path, output_path):
  print("Strip all outputs")


# Strip all actions with cache-hit = true -> easier to investigate cache-miss actions
def stripCacheHit():
  print("hi")

def detectExtensions(str):
  extensions = [".swift", ".h", ".m", ".mm", ".sh", ".js", ".css", ".strings", ".a", ".o", ".png", ".caf", ".wav", ".nib", ".plist", ".json", ".pdf", ".gif", ".car", ".ttf", ".dylib", ".py", ".framework", "protobuf", "/dev/null", ".cer", ".publicKey"]
  for ext in extensions:  
    if str.find(ext) != -1:
      print('Detected {}'.format(ext))
      return True

def detectAcceptAll(str):
  return True

if __name__ == "__main__":
  print("START")
  stripInput(start_token = 'inputs {\n', input_file='bazel_exec_Driver.txt', output_path = 'result1.txt', detector_func=detectExtensions)
  stripInput(start_token = 'actual_outputs {\n', input_file='result1.txt', output_path = 'result2.txt', detector_func=detectAcceptAll)
  print("FINISHED")
