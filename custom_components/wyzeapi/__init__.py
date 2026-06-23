@@
 async def setup_coordinators(
     hass: HomeAssistant, config_entry: ConfigEntry, client: Wyzeapy
 ):
-    """Set up coordinators for Wyze devices that require Bluetooth."""
-    # Check if Bluetooth is active and functioning
+    """Set up coordinators for Wyze Lock Bolt devices (BLE and IoT3)."""
+    from .const import IOT3_MODELS
@@
-    # IoT3 coordinators for DX-family locks (no Bluetooth needed)
-    iot3_locks = iot3_devices
-    if iot3_locks:
-        iot3_service = Iot3Service(hass, config_entry)
-        hass.data[DOMAIN][config_entry.entry_id]["iot3_service"] = iot3_service
-        for lock in iot3_locks:
-            _LOGGER.info(
-                "Setting up IoT3 coordinator for %s (%s)",
-                lock.nickname,
-                lock.product_model,
-            )
-            coordinators[lock.mac] = WyzeLockBoltV2Coordinator(
-                hass, iot3_service, lock
-            )
+    # IoT3 coordinators for DX-family locks (no Bluetooth needed)
+    iot3_locks = iot3_devices
+    if iot3_locks:
+        # Pass the authenticated Wyzeapy client into the service so it can
+        # reuse the client's session and token hooks when available.
+        iot3_service = Iot3Service(hass, config_entry, client)
+        hass.data[DOMAIN][config_entry.entry_id]["iot3_service"] = iot3_service
+        for lock in iot3_locks:
+            _LOGGER.info(
+                "Setting up IoT3 coordinator for %s (%s)",
+                lock.nickname,
+                lock.product_model,
+            )
+            coordinator = WyzeLockBoltV2Coordinator(hass, iot3_service, lock)
+            coordinators[lock.mac] = coordinator
+            # Perform an initial refresh so entities are available immediately
+            try:
+                await coordinator.async_config_entry_first_refresh()
+            except Exception as exc:  # UpdateFailed and other errors
+                _LOGGER.error(
+                    "Initial IoT3 refresh failed for %s (%s): %s",
+                    lock.nickname,
+                    lock.mac,
+                    exc,
+                )
+                # Remove the coordinator so we don't create entities for it
+                coordinators.pop(lock.mac, None)
@@
-    for lock in all_locks:
+    for lock in all_locks:
         if lock.product_model == "YD_BT1":
             coordinators[lock.mac] = WyzeLockBoltCoordinator(hass, lock_service, lock)
             await coordinators[lock.mac].update_lock_info()
