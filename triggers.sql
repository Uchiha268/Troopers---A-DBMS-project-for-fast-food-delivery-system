--Checks if the particular offer_id is indeed under the user or not
delimiter $$
create trigger check_offer
before insert
on
orders
for each row begin
if not exists(select * from user_and_offer where user_id = new.user_id and offer_id = new.offer_id)
then
signal sqlstate'45000'
set message_text = "Cannot add this offer_id because the user is not eligible for it...";
end if;
END $$
delimiter ;

--adds total if payment has not been done yet and also calculates item_total
delimiter $$
create trigger add_food
before insert
on
order_and_food_item
for each row begin
set @actual_franchise = (select franchise_id from orders where order_id = new.order_id);
if(@actual_franchise <> new.franchise_id)
then
signal sqlstate '45000'
set message_text="This order is not from this franchise...";
end if;


set @pri = (select price from food_item where food_id = new.food_id and franchise_id = new.franchise_id);
set new.total_item_price = @pri * new.quantity;
if not exists (select * from payment_info where order_id = new.order_id)
then
update orders set total_amount = total_amount + new.total_item_price
where order_id = new.order_id;

else
signal sqlstate '45000'
set message_text="Cannot add food to an order which has been completed and paid for...";
end if;
END $$
delimiter ;

--same for update
delimiter $$
create trigger add_food_update
before update
on
order_and_food_item
for each row begin
set @actual_franchise = (select franchise_id from orders where order_id = new.order_id);
if(@actual_franchise <> new.franchise_id)
then
signal sqlstate '45000'
set message_text="This order is not from this franchise...";
end if;
set @pri = (select price from food_item where food_id = new.food_id and franchise_id = new.franchise_id);
set new.total_item_price = @pri * new.quantity;
if not exists (select * from payment_info where order_id = new.order_id)
then
update orders set total_amount = total_amount + new.total_item_price
where order_id = new.order_id;

else
signal sqlstate '45000'
set message_text="Cannot add food to an order which has been completed and paid for...";
end if;
END $$
delimiter ;


--reduces total if payment has not been done yet
delimiter $$
create trigger delete_food
before delete
on
order_and_food_item
for each row begin
set @actual_franchise = (select franchise_id from orders where order_id = old.order_id);
if(@actual_franchise <> old.franchise_id)
then
signal sqlstate '45000'
set message_text="This order is not from this franchise...";
end if;
if not exists (select * from payment_info where order_id = old.order_id)
then
update orders set total_amount = total_amount - old.total_item_price
where order_id = old.order_id;

else
signal sqlstate '45000' set message_text="Cannot delete food to an order which has been completed and paid for";
end if;
END $$
delimiter ;

--makes sure the payment is done by the right user and only confirms payment if delivery partners available
delimiter $$
create trigger user_check
before insert
on payment_info
for each row begin
set @user = (select user_id from orders where order_id = new.order_id and not exists (select * from payment_info where order_id = new.order_id) limit 1);
set @new_user = new.user_id;
if @user != new.user_id
then
signal sqlstate '45000' set message_text="This order_id doesn't belong to this user";
end if;
set @delivery_agent = (select agent_id from delivery_agent where available = 1 limit 1);
if @delivery_agent is null
then
signal sqlstate '45000' set message_text="No delivery agents available at this moment...";
else
update delivery_agent set available = 0 where agent_id = @delivery_agent;
insert into order_and_delivery_agent values(new.order_id, @delivery_agent, 0);
end if;

END $$
delimiter ; 

--makes delivery partner available again once food is delivered
delimiter $$
create procedure food_delivered(in cur_order_id int, in cur_agent_id int)
begin
	update order_and_delivery_agent set delivered = 1 where order_id = cur_order_id and agent_id = cur_agent_id;
	update delivery_agent set available = 1 where agent_id = cur_agent_id;
end $$
delimiter ;



--calculate discount
delimiter $$
create trigger discount
before update on orders
for each row begin
set @here = 1;
if (new.offer_id <> 0)
then
set @percent = (select percent from offer where offer_id = new.offer_id);
set @max_discount = (select max_discount from offer where offer_id = new.offer_id);
set new.discount = calculate_discount(@max_discount, @percent, new.total_amount);
end if;
set new.final_price = new.total_amount - new.discount;
end $$
delimiter ;

--function
delimiter $$
create function calculate_discount(max_discount int, percent float, total_amount int)
returns int
deterministic
begin
    declare new_discount int;
    if (total_amount * percent) > max_discount
	then
	set new_discount = max_discount;
	else
	set new_discount = total_amount * percent;
	end if;
    
    return new_discount;
end $$
delimiter ;

Create function get_food_count(franchise bigint)
    returns int
    language plpgsql
    as
    $$
    Declare
    food_count integer;
    Begin
    select count(*) from food_item into food_count where franchise_id = franchise;
    return food_count;
    End;
    $$;

delimiter $$
create trigger check_delivery_agent
before insert on delivery_agent
for each row begin
if not exists (select * from user where user_id = new.user_id)
then
signal sqlstate '45000' set message_text="No such user exists...";
end if;
set @permission = (select permissions from user where user_id = new.user_id);
if @permission <> 'delivery_agent'
then
signal sqlstate '45000' set message_text="This user has not enrolled as a delivery agent...";
end if;
end $$
delimiter ;

delimiter $$
create procedure unassigned_delivery_agents()
begin
    declare done int default 0;
    declare usr varchar(255);
    declare nam varchar(255);
    declare cur cursor for select user_id, name from user where permissions = 'delivery_agent';
    declare continue handler for not found set done = 1;
    open cur;
    label:
        loop
            fetch cur into usr, nam;
            if done = 1 then leave label;
            end if;
            if not exists(select * from delivery_agent where user_id = usr)
            then
            select usr as User_ID, nam as User_Name;
            end if;
        end loop;
    close cur;
end $$
delimiter ;

PREPARE get_user_id (int) AS
    SELECT user_id from orders where order_id = $1;
EXECUTE usrrptplan(1, current_date);








