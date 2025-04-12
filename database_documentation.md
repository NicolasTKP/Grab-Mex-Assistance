# Documentation

## Items Table:

The "Items" table stores detailed information about the individual food items offered by various merchants. Each record in this table represents a single menu item and includes attributes such as the item_id (a unique identifier for each item), item_name (the name of the dish), item_price (the cost of the item), and cuisine_tag (which classifies the item under specific cuisine types like Japanese, Western, Indian, etc.). The merchant_id field links each item to its respective vendor or restaurant, enabling organized tracking and management of offerings per merchant. This table plays a crucial role in menu presentation, pricing analysis, and cuisine-based categorization across the platform.

---

## Merchant Table:

The "Merchant" table contains essential information about each vendor or restaurant registered on the platform. Each entry includes a unique merchant_id used to identify the merchant, along with the merchant_name representing the restaurant or food outlet's name. The join_date records the date the merchant joined the platform, which is useful for tracking vendor activity over time. The city_id serves as a reference to the location or region in which the merchant operates. This table is fundamental in managing vendor relationships, onboarding history, and regional merchant distribution.

---

## Keywords Table:

The "Keywords" table captures user search behavior and engagement metrics across different stages of the customer journey. Each record represents a specific keyword entered by users, accompanied by several key performance indicators: view (the number of times the keyword appeared in search results or was viewed), menu (how often users navigated to a menu after searching the keyword), checkout (instances where the keyword search led to checkout initiation), and order (completed orders associated with the keyword). This table is instrumental in understanding customer intent, optimizing search relevance, and analyzing keyword-to-conversion effectiveness.

---

## Transaction_Items Table:

The "Transaction_Items" table acts as a linkage between customer orders and the specific items included in each purchase. Each entry includes an order_id, identifying the transaction, an item_id referencing the purchased menu item, and a merchant_id indicating the vendor responsible for fulfilling the item. This table enables a detailed breakdown of each order's contents, supporting item-level analysis, order history tracking, and merchant performance evaluation. It is critical for understanding purchase patterns, generating detailed order reports, and managing fulfillment workflows.

## Transaction_Data Table:

The "Transaction_Data" table provides a comprehensive timeline and performance metrics for each food delivery order. Each record is identified by a unique order_id and includes key timestamps such as order_time (when the order was placed), driver_arrival_time (when the driver reached the merchant), driver_pickup_time (when the driver picked up the food), and delivery_time (when the order was delivered to the customer). Additionally, the table tracks financial and operational details such as order_value, the associated merchant_id, and calculated durations like driver_lead_time, order_preparation_time, delivery_duration, driver_idle_time, and total_order_used_time. This dataset is crucial for analyzing delivery efficiency, merchant preparation speed, and overall service performance.