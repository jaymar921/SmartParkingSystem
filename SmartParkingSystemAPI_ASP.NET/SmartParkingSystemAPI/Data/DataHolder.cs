using SmartParkingSystemAPI.Models;

namespace SmartParkingSystemAPI.Data
{
    public class DataHolder: IDataHolder
    {
        private List<Card> CardRepository;
        public DataHolder()
        {
            CardRepository = new List<Card>();

            // register cards 
            CardRepository.Add(new Card() { uid = "1068049966", balance = 0.0, name = "Jayharron Mar Abejar" });
        }

        public List<Card> getAllCards() => CardRepository;
        public void registerCard(Card card)
        {
            CardRepository.Add(card);
        }

        public bool removeCard(string uid)
        {
            Card? toRemove = null;
            foreach(Card card in CardRepository)
            {
                if (card.uid.Equals(uid))
                {
                    toRemove = card;
                    break;
                }
            }
            if (toRemove != null)
            {
                CardRepository.Remove(toRemove);
                return true;
            }
            return false;   
        }

        public bool topUp(string uid, double amount)
        {
            foreach(Card card in CardRepository)
            {
                if (card.uid == uid)
                {
                    card.balance += amount;
                    return true;
                }
            }
            return false;
        }

        public Card getCard(string uid)
        {
            foreach(Card card in CardRepository)
            {
                if (card.uid.Equals(uid)) return card;
            }
            return Card.Empty();
        }

    }
}
