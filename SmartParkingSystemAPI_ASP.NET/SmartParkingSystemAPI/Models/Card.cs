using System.Xml;

namespace SmartParkingSystemAPI.Models
{
    public class Card
    {
        public string uid {get; set;}
        public string name { get; set; }
        public double balance { get; set; }

        public static Card Empty()
        {
            return new Card() { uid = "INVALID", balance = 0.0, name = "" };
        }
    }
}
