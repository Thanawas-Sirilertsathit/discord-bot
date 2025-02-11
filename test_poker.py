from datetime import datetime
from bot import evaluate_hand

def test_straight():
    """Test when card form a straight."""
    hand = ['[ 5 ♦ ]', '[ 6 ♣ ]', '[ 7 ♠ ]', '[ 8 ♥ ]', '[ 9 ♠ ]']
    table_cards = ['[ A ♠ ]']
    
    score, best_hand = evaluate_hand(hand, table_cards)
    
    print(f"Straight Test - Score: {score}, Best Hand: {best_hand}")
    assert score == 5, "Test failed! Expected Straight (score 5)."

    hand = ['[ A ♦ ]', '[ 2 ♣ ]', '[ 3 ♠ ]', '[ 4 ♥ ]', '[ 5 ♠ ]']
    table_cards = []
    
    score, best_hand = evaluate_hand(hand, table_cards)
    
    print(f"Straight Test - Score: {score}, Best Hand: {best_hand}")
    assert score == 5, "Test failed! Expected Straight (score 5)."

    hand = ['[ A ♦ ]', '[ 10 ♣ ]', '[ J ♠ ]', '[ Q ♥ ]', '[ K ♠ ]']
    table_cards = ['[ Q ♠ ]']
    
    score, best_hand = evaluate_hand(hand, table_cards)
    
    print(f"Straight Test - Score: {score}, Best Hand: {best_hand}")
    assert score == 5, "Test failed! Expected Straight (score 5)."

def test_flush():
    """Test when card form a flush"""
    hand = ['[ A ♦ ]', '[ 10 ♦ ]', '[ J ♦ ]', '[ Q ♦ ]', '[ K ♠ ]']
    table_cards = ['[ 2 ♦ ]']
    
    score, best_hand = evaluate_hand(hand, table_cards)
    
    print(f"Flush Test - Score: {score}, Best Hand: {best_hand}")
    assert score == 6, "Test failed! Expected Flush (score 6)."

def test_straight_flush():
    """Test when card form a straight flush."""
    hand = ['[ 4 ♥ ]', '[ 6 ♦ ]', '[ 7 ♦ ]', '[ 8 ♦ ]', '[ 9 ♦ ]']
    table_cards = ['[ 5 ♠ ]', '[ 5 ♦ ]']
    
    score, best_hand = evaluate_hand(hand, table_cards)
    
    # Expected result: Score 9 for Straight Flush
    print(f"Straight Flush Test - Score: {score}, Best Hand: {best_hand}")
    assert score == 9, "Test failed! Expected Straight Flush (score 9)."
    hand = ['[ A ♦ ]', '[ 2 ♦ ]', '[ 3 ♦ ]', '[ 4 ♦ ]', '[ 5 ♦ ]']
    table_cards = []
    
    score, best_hand = evaluate_hand(hand, table_cards)
    
    # Expected result: Score 9 for Straight Flush
    print(f"Straight Flush Test - Score: {score}, Best Hand: {best_hand}")
    assert score == 9, "Test failed! Expected Straight Flush (score 9)."

if __name__ == '__main__':
    test_straight()
    test_straight_flush()
    test_flush()
