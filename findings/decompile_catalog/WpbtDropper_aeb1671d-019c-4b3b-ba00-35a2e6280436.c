/*
 * Module: WpbtDropper
 * GUID: aeb1671d-019c-4b3b-ba00-35a2e6280436
 * Source: /run/media/julian/ML6/bios-re/extracted/fid_rea/flash/FV@0x92f000/FFS-9e21fd93-9c72-4c15-8c4b-e77f1db2d792@0xa1ee78/section-0/section-1/FV@0x10/FFS-aeb1671d-019c-4b3b-ba00-35a2e6280436@0xbc0698/section-0/section-0.payload.bin
 */


// --- Procedure: 0x140001580 ---

void entry(longlong param_1)

{
  short *psVar1;
  short sVar2;
  ushort uVar3;
  int iVar4;
  longlong lVar5;
  short *psVar6;
  undefined1 *puVar7;
  longlong lVar8;
  undefined8 ******ppppppuVar9;
  wchar_t *pwVar10;
  undefined4 uVar11;
  int *piVar12;
  undefined8 *****pppppuStackX_8;
  int aiStack_4a8 [4];
  undefined1 auStack_498 [16];
  undefined4 auStack_488 [2];
  undefined8 uStack_480;
  undefined1 *puStack_478;
  undefined4 uStack_470;
  undefined8 uStack_468;
  undefined8 uStack_460;
  undefined8 uStack_458;
  undefined8 uStack_450;
  undefined8 uStack_448;
  undefined8 uStack_440;
  undefined8 uStack_438;
  undefined8 uStack_430;
  undefined8 uStack_428;
  wchar_t awStack_418 [255];
  undefined1 auStack_21a [2];
  wchar_t awStack_218 [256];
  
  if (param_1 == 0) {
    return;
  }
  uStack_428 = 0;
  uStack_450 = 0;
  uStack_448 = 0;
  uStack_440 = 0;
  uStack_458 = 0x38;
  uStack_438 = 0;
  uStack_430 = 0;
  lVar5 = RtlCreateHeap(2,0,0x1000000,0x1000,0,&uStack_458);
  if (lVar5 == 0) {
    NtTerminateProcess(0xffffffffffffffff,0);
    RtlDestroyHeap(0);
    return;
  }
  pwVar10 = awStack_418;
  for (lVar8 = 0xff; lVar8 != 0; lVar8 = lVar8 + -1) {
    *pwVar10 = L'\0';
    pwVar10 = pwVar10 + 1;
  }
  builtin_wcsncpy(awStack_418,L"\\SystemR",8);
  pwVar10 = awStack_218;
  for (lVar8 = 0xff; lVar8 != 0; lVar8 = lVar8 + -1) {
    *pwVar10 = L'\0';
    pwVar10 = pwVar10 + 1;
  }
  builtin_wcsncpy(awStack_418 + 8,L"oot\\System32\\GigabyteUpdateService.exe",0x27);
  RtlInitUnicodeString(auStack_498,awStack_418);
  puStack_478 = auStack_498;
  piVar12 = aiStack_4a8;
  uVar11 = SUB84(auStack_488,0);
  ppppppuVar9 = &pppppuStackX_8;
  lVar8 = 0x40100000;
  auStack_488[0] = 0x30;
  uStack_480 = 0;
  uStack_470 = 0x40;
  uStack_468 = 0;
  uStack_460 = 0;
  iVar4 = NtCreateFile();
  if (-1 < iVar4) {
    if (-1 < aiStack_4a8[0]) {
      piVar12 = (int *)0x0;
      uVar11 = 0;
      lVar8 = 0;
      ppppppuVar9 = (undefined8 ******)pppppuStackX_8;
      iVar4 = NtWriteFile();
      if ((iVar4 < 0) ||
         ((-1 < aiStack_4a8[0] &&
          (iVar4 = NtClose(), ppppppuVar9 = (undefined8 ******)pppppuStackX_8, iVar4 < 0))))
      goto LAB_1400012c2;
    }
    builtin_wcsncpy(awStack_218,L"%SystemRoot%\\sys",0x10);
    awStack_218[0x30] = 0;
    builtin_wcsncpy(awStack_218 + 0x10,L"tem32\\GigabyteUpdateService.exe ",0x20);
    if (*(short *)(*(longlong *)(param_1 + 0x20) + 0x70) != 0) {
      psVar6 = *(short **)(*(longlong *)(param_1 + 0x20) + 0x78);
      sVar2 = *psVar6;
      while (sVar2 != 0x20) {
        psVar6 = psVar6 + 1;
        sVar2 = *psVar6;
      }
      puVar7 = auStack_21a;
      do {
        psVar1 = (short *)(puVar7 + 2);
        puVar7 = puVar7 + 2;
      } while (*psVar1 != 0);
      lVar8 = 0;
      do {
        uVar3 = psVar6[lVar8 + 1];
        ppppppuVar9 = (undefined8 ******)(ulonglong)uVar3;
        *(ushort *)(puVar7 + lVar8 * 2) = uVar3;
        lVar8 = lVar8 + 1;
      } while (uVar3 != 0);
    }
    FUN_140001300(ppppppuVar9,lVar8,uVar11,piVar12,(longlong)awStack_218);
  }
LAB_1400012c2:
  RtlDestroyHeap(lVar5);
  NtTerminateProcess(0xffffffffffffffff,0);
  return;
}




// --- Procedure: 0x140001300 ---

ulonglong FUN_140001300(undefined8 param_1,undefined8 param_2,undefined4 param_3,undefined8 param_4,
                       longlong param_5)

{
  longlong lVar1;
  ulonglong uVar2;
  longlong lVar3;
  undefined4 local_res18 [2];
  undefined8 local_res20;
  undefined1 local_58 [16];
  undefined1 local_48 [16];
  undefined4 local_38 [2];
  undefined8 local_30;
  undefined1 *local_28;
  undefined4 local_20;
  undefined8 local_18;
  undefined8 uStack_10;
  
  local_res18[0] = param_3;
  local_res20 = param_4;
  RtlInitUnicodeString
            (local_48,
             L"\\Registry\\Machine\\System\\CurrentControlSet\\Services\\GigabyteUpdateService");
  RtlInitUnicodeString
            (local_58,
             L"\\Registry\\Machine\\System\\CurrentControlSet\\Services\\GigabyteUpdateService");
  local_38[0] = 0x30;
  local_28 = local_48;
  local_30 = 0;
  local_20 = 0x240;
  local_18 = 0;
  uStack_10 = 0;
  uVar2 = NtCreateKey(&local_res20,0xf003f,local_38,0,0,1,0);
  if (-1 < (int)uVar2) {
    RtlInitUnicodeString(local_58,L"DisplayName");
    NtSetValueKey(local_res20,local_58,0,1,L"GIGABYTE Update Service",0x30);
    RtlInitUnicodeString(local_58,L"ObjectName");
    NtSetValueKey(local_res20,local_58,0,1,L"LocalSystem",0x18);
    local_res18[0] = 1;
    RtlInitUnicodeString(local_58,L"ErrorControl");
    NtSetValueKey(local_res20,local_58,0,4,local_res18,4);
    local_res18[0] = 2;
    RtlInitUnicodeString(local_58,L"Start");
    NtSetValueKey(local_res20,local_58,0,4,local_res18,4);
    local_res18[0] = 0x10;
    RtlInitUnicodeString(local_58,L"Type");
    NtSetValueKey(local_res20,local_58,0,4,local_res18,4);
    RtlInitUnicodeString(local_58,L"ImagePath");
    lVar3 = -1;
    do {
      lVar1 = lVar3 * 2;
      lVar3 = lVar3 + 1;
    } while (*(short *)(param_5 + 2 + lVar1) != 0);
    NtSetValueKey(local_res20,local_58,0,2,param_5,(int)lVar3 * 2 + 2);
    local_res18[0] = 1;
    RtlInitUnicodeString(local_58,L"Handshake");
    NtSetValueKey(local_res20,local_58,0,4,local_res18,4);
    NtClose(local_res20);
    uVar2 = uVar2 & 0xffffffff;
  }
  return uVar2;
}



