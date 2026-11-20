/*
 * Module: SmBusPei
 * GUID: 0af9b07a-f8bd-1040-a434-4329fb61330d
 * Architecture: IA32 (PEIM)
 * Decompiled with REA + Ghidra 12.1.4
 */

#include <PiPei.h>
#include <Ppi/Smbus2.h>

// --- Procedure: _EntryPoint (0x80 / RVA 0x2c0) ---
void _EntryPoint(EFI_PEI_FILE_HANDLE FileHandle, const EFI_PEI_SERVICES **PeiServices)
{
  EFI_STATUS Status;
  void *Pool1;
  void *Pool2;

  // Allocate SMBus controller descriptor 1 (Port 0xB00)
  Status = (*PeiServices)->AllocatePool(PeiServices, 0x58, &Pool1);
  if (Status < 0) return;
  Status = (*PeiServices)->AllocatePool(PeiServices, 0xA0, (UINT8 *)Pool1 + 0x3C);
  if (Status < 0) return;

  // Set I/O Base Port to 0x0B00
  *(UINT16 *)((UINT8 *)Pool1 + 0x28) = 0x0B00;

  // Query AMD Fabric PPI (1f4c6f90-b06b-48d8-a201-bae5f1cd7d56)
  Status = (*PeiServices)->LocatePpi(PeiServices, &gAmdFabricPpiGuid, 0, NULL, (void **)((UINT8 *)Pool1 + 0x20));
  if (Status >= 0) {
    // Configure FCH MMIO
    _FchMmioInit();

    // Register EndOfPei Notifier
    Status = (*PeiServices)->NotifyPpi(PeiServices, (EFI_PEI_NOTIFY_DESCRIPTOR *)((UINT8 *)Pool1 + 0x40));

    // Install gEfiPeiSmbus2PpiGuid
    if (Status >= 0) {
      Status = (*PeiServices)->InstallPpi(PeiServices, (EFI_PEI_PPI_DESCRIPTOR *)((UINT8 *)Pool1 + 0x4C));
    }
  }
}

// --- Procedure: _FchMmioInit (0xb19) ---
void _FchMmioInit(void)
{
  *(volatile UINT8 *)0xFED80304 |= 0x02;
  *(volatile UINT8 *)0xFED80302 |= 0x01;
  *(volatile UINT8 *)0xFED80300 |= 0x10;
}

// --- Procedure: _SmbusExecute (0x506) ---
EFI_STATUS EFIAPI _SmbusExecute(EFI_PEI_SMBUS2_PPI *This, EFI_SMBUS_DEVICE_ADDRESS SlaveAddress,
                               UINTN Command, EFI_SMBUS_OPERATION Operation,
                               BOOLEAN PecCheck, UINTN *Length, VOID *Buffer)
{
  return _SmbusExecuteCore(This, SlaveAddress, Command, Operation, PecCheck, Length, Buffer);
}

// --- Procedure: _SmbusExecuteCore (0xa34) ---
EFI_STATUS _SmbusExecuteCore(EFI_PEI_SMBUS2_PPI *This, EFI_SMBUS_DEVICE_ADDRESS SlaveAddress,
                            UINTN Command, EFI_SMBUS_OPERATION Operation,
                            BOOLEAN PecCheck, UINTN *Length, VOID *Buffer)
{
  UINT8 AddrByte = (SlaveAddress.SmbusDeviceAddress & 0x7F) << 1;
  UINT16 IoBase = *(UINT16 *)((UINT8 *)This + 0x28);
  return _SmbusIoTransaction(IoBase, AddrByte, Command, Operation, Length, Buffer);
}

// --- Procedure: _SmbusIoTransaction (0xecf) ---
EFI_STATUS _SmbusIoTransaction(UINT16 IoBase, UINT8 AddrByte, UINTN Command,
                              EFI_SMBUS_OPERATION Operation, UINTN *Length, VOID *Buffer)
{
  IoWrite8(IoBase + 0x04, AddrByte | (Operation & 1));
  IoWrite8(IoBase + 0x03, (UINT8)Command);
  IoWrite8(IoBase + 0x02, 0x40 | ((Operation >> 1) << 2)); // Start transaction
  return _SmbusPollStatus(IoBase);
}

// --- Procedure: _SmbusPollStatus (0xe7e) ---
EFI_STATUS _SmbusPollStatus(UINT16 IoBase)
{
  UINT8 Status;
  do {
    Status = IoRead8(IoBase + 0x00);
    if (Status & 0x1C) { // Error bits: BUS_ERR | DEV_ERR | COLLISION
      IoWrite8(IoBase + 0x00, Status);
      return EFI_DEVICE_ERROR;
    }
  } while (Status & 0x01); // Poll Host Busy
  return EFI_SUCCESS;
}
