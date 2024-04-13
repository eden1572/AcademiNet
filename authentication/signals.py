from django.dispatch import Signal


#מנגנון שמשאפשר לשלוט על אירועים במערכת 
#מאפשר לשלוח התרעה למנהל או לעדכן פרטים במסד הנתונים
user_recovers_password = Signal() 
