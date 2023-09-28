import razorpay
client = razorpay.Client(auth=("rzp_test_3o4uCTy7o49u1o", "0I2hQKqbps97LEmNCBqBClpc"))

res = client.payment_link.create({
    "upi_link": False,
    "amount": 108,
    "currency": "INR",
    "accept_partial": False,
    "description": "For Gita Daily 1 month subscription",
    "customer": {
        "name": "Samarth",
        "contact": "917337610771",
    },
    "notify": {
        "sms": True,
        "email": True
    },
    "reminder_enable": False,
})  

# res = client.payment_link.fetch("plink_MgtKJnjX7etcnX")


print(res)