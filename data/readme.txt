CUAD Dataset Information
=========================

Overview
--------
The Contract Understanding Atticus Dataset (CUAD) is a collection of U.S. government contracts annotated for common contract review questions. It was created to support legal‐tech applications, particularly those involving contract analysis and review automation.

Key Details
-----------
- **Full Name**: Contract Understanding Atticus Dataset  
- **Abbreviation**: CUAD  
- **Publisher**: Legal AI Lab, Cornell University  
- **Original Format**: JSON  
- **Size**: Approximately 510 contracts, each broken into paragraphs and Q&A annotations  
- **Annotations**: Each contract entry includes a "title" field and a "paragraphs" list. Under each paragraph, there is a "qas" list containing question‐answer pairs. Each “answer” object has a text span (the clause) and its start index in the contract.

License
-------
CUAD is distributed under an open license for academic and commercial use. Please refer to the original CUAD repository for full license details:
https://github.com/TheAtticusProject/cuad

Renaming to cuad.json
---------------------
1. **Download the CUAD JSON file**  
   - Clone or download the official CUAD repository:  
     ```bash
     git clone https://github.com/TheAtticusProject/cuad.git
     ```  
   - Inside the cloned repo, locate the dataset file (often named `train.json`, `dev.json`, or similar). For simplicity, you may use `train.json` as the primary source for indexing.

2. **Rename the file**  
   - Copy or move the downloaded JSON into this project’s `data/` directory and rename it to `cuad.json`. For example:  
     ```bash
     mkdir -p data
     cp ../cuad/train.json data/cuad.json
     ```  
     _Adjust the source path (`../cuad/train.json`) to wherever you downloaded the dataset file._

3. **Verify structure**  
   - Open `data/cuad.json` in a text editor or run:  
     ```bash
     head -n 20 data/cuad.json
     ```  
   - Ensure you see an object with keys similar to:  
     ```json
     {
       "version": "some_version_identifier",
       "data": [
         {
           "title": "Contract_Title_1",
           "paragraphs": [
             {
               "qas": [
                 {
                   "id": "Contract_Title_1__Some_Question",
                   "question": "What is the payment clause?",
                   "answers": [
                     {
                       "text": "Payment shall be due within 30 days of invoice receipt.",
                       "answer_start": 1234
                     }
                   ],
                   "is_impossible": false
                 },
                 ...
               ]
             },
             ...
           ]
         },
         ...
       ]
     }
     ```

4. **Proceed with indexing**  
   - Once `data/cuad.json` is in place and correctly formatted, run the indexing script:  
     ```bash
     python build_index.py
     ```  
   - The script will extract all `"answers[].text"` fields (i.e., the contract clauses) for embedding and storage in Qdrant.

Notes
-----
- If you only have separate `train.json` and `dev.json`, you can merge them into a single `cuad.json` by concatenating their `"data"` arrays. For example:
  ```python
  import json

  with open("train.json") as f_train, open("dev.json") as f_dev:
      train_data = json.load(f_train)
      dev_data = json.load(f_dev)

  merged = {
      "version": train_data.get("version", dev_data.get("version")),
      "data": train_data["data"] + dev_data["data"]
  }

  with open("data/cuad.json", "w") as f_out:
      json.dump(merged, f_out, indent=2)
