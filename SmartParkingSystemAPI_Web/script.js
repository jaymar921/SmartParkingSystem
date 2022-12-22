'use strict';

// defined attributes
const STATUS_DISPLAY = document.getElementById('api-status')
let API_INPUT = document.getElementById('connect_api');
let ROW_DIV = document.getElementById('card-rows');
let interval_id = ''
// connect to the API
function connectAPI(){
    if(!API_INPUT.value)
        return;
    fetch(API_INPUT.value, { 
            headers:{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin" : "*"
            },
            method:'GET'
        }).then( response =>{
        API_INPUT.disabled = true;
        STATUS_DISPLAY.innerHTML = 'CONNECTED';
        STATUS_DISPLAY.style.color = 'yellowgreen';
        APISessionStart();
        interval_id = setInterval(APISessionStart, 2000);
    }).catch( err => {
        STATUS_DISPLAY.innerHTML = 'FAILED TO CONNECT';
        STATUS_DISPLAY.style.color = 'red';
        API_INPUT.disabled = false;
    })
}

async function APISessionStart(){
    try{
        const response = await fetch(`${API_INPUT.value}api/cards`, {
            headers:{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin" : "*"
            },
            method:'GET'
        });
    
        const data = await response.json();
        
        data.map( card => {
            const {uid, name, balance} = card
            addCardToList(uid, name, balance);
        });
    }catch(err){
        STATUS_DISPLAY.innerHTML = 'FAILED TO CONNECT';
        STATUS_DISPLAY.style.color = 'red';
        API_INPUT.disabled = false;
        clearInterval(interval_id);
    }
}

async function updateCard(){
    const name = document.getElementById('user-name').value;
    const uid = document.getElementById('user-uid').value;
    const balance = document.getElementById('user-balance').value;

    await fetch(`${API_INPUT.value}api/cards`,
        {   method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin" : "*"
            },
            body: JSON.stringify({
                balance, name, uid
            })
        })
    
    updateCardFromList(uid, name, balance);
}
function formatToCurrency(amount){
    return (amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'); 
}

function updateModal(...data){
    document.getElementById('user-name').value = data[0];
    document.getElementById('user-uid').value = data[1];
    document.getElementById('user-balance').value = data[2];
    document.getElementById('card-rows').classList.add('blur');
    document.getElementById('update-modal').style.display = 'block';
}

function closeModal(){
    document.getElementById('card-rows').classList.remove('blur');
    document.getElementById('update-modal').style.display = 'none';
}

function addCardToList(uid, name, balance){
    const COLUMN_DIV_ELEMENT = document.createElement('div');
    COLUMN_DIV_ELEMENT.classList.add('col-lg-3');
    COLUMN_DIV_ELEMENT.classList.add('col-md-4');
    COLUMN_DIV_ELEMENT.classList.add('col-sm-6');

    const CARD_DIV_ELEMENT = document.createElement('div');
    CARD_DIV_ELEMENT.classList.add('card');
    CARD_DIV_ELEMENT.id = `UID${uid}`;
    //CARD_DIV_ELEMENT.onclick = `updateModal([${name}, ${uid}, ${balance}])`;
    //CARD_DIV_ELEMENT.onclick = updateModal([name, uid, balance]);
    CARD_DIV_ELEMENT.setAttribute('onclick', `updateModal('${name}', '${uid}', ${balance})`)

    const CARD_TITLE = document.createElement('H2');
    CARD_TITLE.innerHTML = name;
    CARD_TITLE.id = `UID${uid}NAME`;

    const CARD_UID = document.createElement('p');
    CARD_UID.innerHTML = `Card ID: ${uid}`

    const CARD_BALANCE = document.createElement('p');
    CARD_BALANCE.innerHTML = `Balance: <b>₱${formatToCurrency(Number.parseFloat(balance))}</b>`
    CARD_BALANCE.id = `UID${uid}BALANCE`;

    CARD_DIV_ELEMENT.appendChild(CARD_TITLE);
    CARD_DIV_ELEMENT.appendChild(CARD_UID);
    CARD_DIV_ELEMENT.appendChild(CARD_BALANCE);

    COLUMN_DIV_ELEMENT.appendChild(CARD_DIV_ELEMENT);
      
    // check if child already has the same content
    if(document.querySelector(`#UID${uid}`) == null)
        ROW_DIV.appendChild(COLUMN_DIV_ELEMENT);
    // update balance
    BAL_DIV = document.querySelector(`#UID${uid}BALANCE`)
    if (BAL_DIV.innerHTML != `Balance: <b>₱${formatToCurrency(Number.parseFloat(balance))}</b>`)
        BAL_DIV.innerHTML = `Balance: <b>₱${formatToCurrency(Number.parseFloat(balance))}</b>`;
}

function updateCardFromList(uid, name, balance){
    document.getElementById(`UID${uid}NAME`).innerHTML = name;
    document.getElementById(`UID${uid}BALANCE`).innerHTML = `Balance: <b>₱${formatToCurrency(Number.parseFloat(balance))}</b>`;
}

async function deleteCard(){
    const uid = document.getElementById('user-uid').value;
    await fetch(`${API_INPUT.value}api/cards`,
    {   method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin" : "*"
        },
        body: JSON.stringify({
            uid
        })
    })
    if(document.querySelector(`#UID${uid}`) != null){
        ROW_DIV.removeChild(document.querySelector(`#UID${uid}`).parentNode);
    }
    closeModal();
}
