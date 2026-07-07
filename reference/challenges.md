Problem: how to convert JSON input to dataframe
Solution: create function where the list of dictionaries is passed in, a clean dictionary is made with the data we want using "<name>" : dict["<name>"] for key value pair

Problem: after getting the df, need to make sure the architecture of retrieving transactions is stable
Solution: we should not pull duplicate transactions each time, so do the retrieval of data once and then repeat transactions retrieval each time