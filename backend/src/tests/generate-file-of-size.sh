# 1 amount 2 size
dd if=/dev/zero of=output.dat  bs=1$2  count=$1
