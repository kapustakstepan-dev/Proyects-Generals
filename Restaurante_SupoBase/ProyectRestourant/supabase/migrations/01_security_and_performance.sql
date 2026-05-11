-- 01_security_and_performance.sql

-- Indices
create index idx_orders_user on public.orders(user_id);
create index idx_order_items_order on public.order_items(order_id);
create index idx_reservations_user on public.reservations(user_id);

-- Enable RLS
alter table public.users enable row level security;
alter table public.menu enable row level security;
alter table public.orders enable row level security;
alter table public.order_items enable row level security;
alter table public.reservations enable row level security;

-- Policies
create policy "Users can read own profile" on public.users for select using (auth.uid() = id);
create policy "Users can update own profile" on public.users for update using (auth.uid() = id);
create policy "Anyone can read menu" on public.menu for select using (true);
create policy "Users can read own orders" on public.orders for select using (auth.uid() = user_id);
create policy "Users can insert own orders" on public.orders for insert with check (auth.uid() = user_id);
create policy "Users can read own order items" on public.order_items for select using (
  exists (select 1 from public.orders where id = order_items.order_id and user_id = auth.uid())
);
create policy "Users can insert own order items" on public.order_items for insert with check (
  exists (select 1 from public.orders where id = order_items.order_id and user_id = auth.uid())
);
create policy "Users can read own reservations" on public.reservations for select using (auth.uid() = user_id);
create policy "Users can insert own reservations" on public.reservations for insert with check (auth.uid() = user_id);

-- Trigger for Auto-Profile
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.users (id, nickname, role)
  values (new.id, split_part(new.email, '@', 1), 'user')
  on conflict (id) do nothing;
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
