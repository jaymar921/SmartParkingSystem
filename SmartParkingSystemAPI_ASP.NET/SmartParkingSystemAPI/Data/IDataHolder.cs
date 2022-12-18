using SmartParkingSystemAPI.Models;

namespace SmartParkingSystemAPI.Data
{
    public interface IDataHolder
    {
        public List<Card> getAllCards();
        public bool removeCard(string uid);
        public void registerCard(Card card);
        public bool topUp(string uid, double amount);
        public Card getCard(string uid);
    }
}
