from stockList import stock_list

def batch_list():
    batch_size = 10
    stock_batch =[]

    for i in range(0,len(stock_list),batch_size):
        stock = stock_list[i:i+batch_size]
        stock_batch_list = []

        for s in stock:
            stock_batch_list.append(s)
        stock_batch.append(stock_batch_list)
    return stock_batch
