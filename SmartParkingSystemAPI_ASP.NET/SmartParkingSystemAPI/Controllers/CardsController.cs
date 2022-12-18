using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using SmartParkingSystemAPI.Data;
using SmartParkingSystemAPI.Models;
using System.Security.Cryptography.X509Certificates;

namespace SmartParkingSystemAPI.Controllers
{
    [DisableCors]
    [Route("api/[controller]")]
    [ApiController]
    public class CardsController : ControllerBase
    {
        private readonly IDataHolder dataHolder;

        public CardsController(IDataHolder dataHolder)
        {
            this.dataHolder = dataHolder;
        }

        [DisableCors]
        [HttpGet]
        public async Task<ActionResult<Card>> Get()
        {
            try
            {
                var results = dataHolder.getAllCards();
                return Ok(results);
            }
            catch (Exception)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, "Database Failure");
            }
        }

        [DisableCors]
        [HttpGet("{uid}")]
        public async Task<ActionResult<Card>> Get(string uid)
        {
            try
            {
                var results = dataHolder.getCard(uid);
                return Ok(results);
            }
            catch (Exception)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, "Database Failure");
            }
        }

        [DisableCors]
        [HttpPost]
        public ActionResult<Card> Post (Card card)
        {
            try
            {
                // check if cad already registered
                Card existing = dataHolder.getCard(card.uid);
                if (existing.uid.Equals(card.uid) || existing == Card.Empty())
                    return BadRequest("Card UID in use");

                dataHolder.registerCard(card);
                return Created($"/api/cards/{card.uid}", card);
            }
            catch (Exception)
            {
                return BadRequest("An Error occurred");
            }
        }

        [DisableCors]
        [HttpPut]
        public ActionResult<Card> ReloadAndUpdateCard(Card reloadCard)
        {
            try
            {
                Card card = dataHolder.getCard(reloadCard.uid);
                if (card == Card.Empty())
                    return BadRequest("Invalid Card");
                
                card.balance += reloadCard.balance;
                card.name = reloadCard.name;
                return Ok("Card Updated");
            }
            catch (Exception)
            {
                return BadRequest("An Error occurred");
            }
        }

        [DisableCors]
        [HttpDelete]
        public ActionResult<Card> delete(Card card)
        {
            try
            {
                Card toRemove = dataHolder.getCard(card.uid);
                if (toRemove == Card.Empty())
                    return BadRequest("Card Not Found");

                dataHolder.removeCard(toRemove.uid);
                return Ok("Card removed");

            }
            catch (Exception)
            {
                return BadRequest("An Error occurred");
            }
        }
    }
}
