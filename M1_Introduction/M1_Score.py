import argparse
import wer

class SER:
    
    title = 'Sentence Error Rate'
    N = 0
    err = 0
    
class WER:
    
    title= 'Word Error Rate'
    N=0
    err=0
    sub=0
    dele=0
    ins=0

def id(ref=None):
    
    if ref is None:
        RuntimeError("ref is required, cannot be None")
        
    n1 = ref.find("(") #We search the beguinning of the id
    n2 = ref.find(")") #We search the end of the id
        
    ID = ref[n1:n2+1]
    
    return ID

def utTera(s=None):
    
    if s is None:
        RuntimeError("string is required, cannot be None")
        
    utter=s[0:s.find("(")-1]
    
    return utter

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=reference_string, hyp=hypothesis_string)
#
def score(ref_trn=None, hyp_trn=None):
    
    ser = SER() #We create the variable SER to save all the data 
    wer1 = WER() #We create the variable SER to save all the data 
    
    with open (hyp_trn) as f:
        hyp_data = f.readlines()
        f.close()   # just to be explicit
        
    with open (ref_trn) as f:
        ref_data = f.readlines()
        f.close()
        
    
        
    for i in range(0,len(ref_data)):
        # We read the idea from the string
        ID= id(ref_data[i])
        print("id: {}".format(ID)) # We show the results as shown in the example
        
        # We separate the part of the string with the utterance of the id
        words_ref = utTera(ref_data[i])
        words_hyp = utTera(hyp_data[i])
        
        # We separate the words forming an array with a unique word in each position
        words_ref = words_ref.split(" ")
        words_hyp = words_hyp.split(" ")
        
        # We call the function given to calculate the errors
        num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(words_ref, words_hyp)
        
        # We show the results as shown in the example
        print('Scores: N={}, S={}, D={}, I={}\n'.format(num_tokens, num_substitutions, num_deletions, num_insertions))
        
        # We update the SER 
        ser.N += 1;
        if num_errors > 1:
            ser.err += 1
        # We update the WER
        wer1.N += num_tokens
        wer1.err += num_errors
        wer1.sub += num_substitutions
        wer1.dele += num_deletions
        wer1.ins += num_insertions
        
    print('-----------------------------------')
    print('{}:\nSum: N={}, Err={}\nAvg: N={}, Err={:.2f}%'.format(ser.title, ser.N, ser.err, ser.N, (ser.err/ser.N)*100))
    print('-----------------------------------')
    print('{}:\nSum: N={}, Err={}, Sub={}, Del={}, Ins={}'.format(wer1.title, wer1.N, wer1.err, wer1.sub, wer1.dele, wer1.ins))
    print('Avg: N={}, Err={:.2f}%, Sub={:.2f}%, Del={:.2f}%, Ins={:.2f}%'.format(wer1.N, (wer1.err/wer1.N)*100, (wer1.sub/wer1.N)*100, (wer1.dele/wer1.N)*100, (wer1.ins/wer1.N)*100))
    print('-----------------------------------')
        
    return


if __name__=='__main__':
    
    # parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
    #                                               "Computes Word Error Rate and Sentence Error Rate")
    # parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    # parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    # args = parser.parse_args()
    
    hyptrn = 'misc/hyp.trn'
    reftrn = 'misc/ref.trn'
    
    if reftrn is None or hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=reftrn, hyp_trn=hyptrn)
