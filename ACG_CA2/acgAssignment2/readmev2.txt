1. Run two separate terminals
2. CD to the server directory (using terminal 1)
   2.1  Server directory should contain server.py and menu_today.txt files
3. Type "python server.py"
   3.1 You will be prompted to enter the password for the database. The password is 'great stuff'.
   3.2 You will be prompted on whether you would like to view/edit the encrypted data. 
      If you would like to, enter y and the name of the file you would like to edit or view. 
      Enter 1 to view and 2 to edit. If you would not like to view/edit, enter anything other than y.
   3.2  You should see:-
	a.   Socket Created
        b.   Socket bind complete
        c.   Socket now listening
   	Your server program is successfully setup and is 
        listening for connection now
4. CD to the client directory (using terminal 2)
   4.3  Client directory should contain client.py and
        day_end.csv files
5. Type "python client.py"
   5.1 You will be prompted to enter the password for the database. The password is 'great stuff'.
   5.2 You will be prompted on whether you would like to view/edit the encrypted data. 
      If you would like to, enter y and the name of the file you would like to edit or view. 
      Enter 1 to view and 2 to edit. If you would not like to view/edit, enter anything other than y.
   5.3  You should see:-
	a. Menu today received from server
   	b. Sale of the day sent to server
   5.2  menu.csv recevied by client
   5.3  Connection terminated and back to command prompt
6. File "result-<IP Address>" received by server


