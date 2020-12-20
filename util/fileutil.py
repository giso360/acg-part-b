import json
import os

from datasketch import HyperLogLog
from probables import CountMinSketch, HeavyHitters

from util.TweetApproximate import TweetApproximate


def higher_order_func(s, ds):
    a = json.loads(s)
    ds.append(a.get("name"))
    print(s)


def get_screen_name_callback(s, ds):
    a = json.loads(s)
    ds.append(a["user"]["screen_name"])


def get_hashtags_callback(s, ds):
    a = json.loads(s)
    tags = a.get("entities").get("hashtags")
    for tag in tags:
        ds.append(tag["text"])


def process_directory(dir_name, callback, chunk_size=1000):
    files = [dir_name + "/" + file for file in os.listdir(dir_name)]
    file_counter, batches, entity_pool = 0, 0, []
    print("TOTAL FILES PROCESSED: ", len(files))
    for file in files:
        file_counter = file_counter + 1
        print("==============================================================")
        print("Processing File: ", file_counter)
        print("==============================================================")
        final_data_store, total_batches_used = read_file_in_chunks_of_lines_accurate(file, 'utf8', chunk_size, callback)
        batches = batches + total_batches_used
        entity_pool.append(final_data_store)
    print("TOTAL NUMBER OF BATCHES USED: ", batches)
    return entity_pool


def process_directory_approximate(dir_name, chunk_size=2, **method):
    files = [dir_name + "/" + file for file in os.listdir(dir_name)]
    file_counter, batches, entity_pool = 0, 0, []
    print("TOTAL FILES PROCESSED: ", len(files))
    method_used = TweetApproximate(**method)
    for file in files:
        file_counter = file_counter + 1
        print("==============================================================")
        print("Processing File: ", file_counter)
        print("==============================================================")
        final_data_store_approx, total_batches_used_approx = read_file_in_chunks_of_lines_approximate(file, 'utf8', chunk_size,
                                                                                        method_used)
        batches = batches + total_batches_used_approx
        entity_pool.append(final_data_store_approx)
    print("TOTAL NUMBER OF BATCHES USED: ", batches)
    return entity_pool


def read_file_in_chunks_of_lines_accurate(file_name, encoding, chunk_size, callback):
    file = open(file_name, 'r', encoding=encoding)
    counter, batch_counter = 0, 0
    data_store, ds = [], []
    while counter < chunk_size:
        a = file.readline()
        if a != "":
            callback(a, ds)
            counter = counter + 1
            if counter == chunk_size:
                data_store.append(ds)
                ds, counter, batch_counter = [], 0, batch_counter + 1
        else:
            data_store.append(ds)
            break
    print("Stats for processing file: ", file_name)
    print("--------------------------------------------------------------")
    print("Batches used: ", batch_counter)
    print("Size of each batch: ", chunk_size)
    print("Elements of last batch: ", counter)
    print("Total elements/tweets processed: ", (batch_counter * chunk_size) + counter)

    return [e for e in data_store if len(e) > 0], batch_counter


def read_file_in_chunks_of_lines_approximate(file_name, encoding, chunk_size, method):
    file = open(file_name, 'r', encoding=encoding)
    counter, batch_counter = 0, 0
    data_store, ds = [], []
    while counter < chunk_size:
        a = file.readline()
        if a != "":
            a = json.loads(a)
            method.add(a["user"]["screen_name"])
            ds.append(method)
            counter = counter + 1
            if counter == chunk_size:
                data_store.append(ds)
                ds, counter, batch_counter = [], 0, batch_counter + 1
        else:
            data_store.append(ds)
            break
    print("Stats for processing file: ", file_name)
    print("--------------------------------------------------------------")
    print("Batches used: ", batch_counter)
    print("Size of each batch: ", chunk_size)
    print("Elements of last batch: ", counter)
    print("Total elements/tweets processed: ", (batch_counter * chunk_size) + counter)

    return [e for e in data_store if len(e) > 0], batch_counter



