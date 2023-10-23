# usage
```
shell_script = 'performance_android_func.sh'
result_file = 'result_%d_%s.txt' % (version, func_type)
cmd = 'bash %s %s %s' % (shell_script, func_type, result_file)
with open(result_file, "w") as log:
    process = subprocess.Popen(cmd, shell=True, stdout=log, stderr=log)
    process.communicate()
```
# output
![image](https://github.com/tomtomjerry/android_perf_test/assets/25520470/ca6ed376-fa61-4893-be32-503d9f9b51e6)

![image](https://github.com/tomtomjerry/android_perf_test/assets/25520470/945e56e7-fa86-4994-a660-e67f111d3d4a)

![image](https://github.com/tomtomjerry/android_perf_test/assets/25520470/0a675cfd-2e85-4aa7-a858-60fde20dc88f)


