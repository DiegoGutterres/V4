import time 


start_time = time.time()

print('-'*50)
time.sleep(2)

end_time = time.time()

elapsed_time = end_time - start_time
print('finalizado  ==> {:.2f}'.format(elapsed_time))