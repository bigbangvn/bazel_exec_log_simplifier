# bazel_exec_log_simplifier

# To investigate Bazel cache miss issue we need to parse execution log and compare to check which input changes
# Because the log file is usually very big (x0MB) and there're alot of files that we know they don't change (because we can see git log)
# So stripping all of them will make the log file much smaller and easier to investigate the cause of Bazel cache-miss issue