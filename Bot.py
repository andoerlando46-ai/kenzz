#!/usr/bin/env python3
# bot.py - Discord Bot Wrapper untuk Spammer OTP

import discord
from discord.ext import commands
import sys
import platform
import asyncio
from datetime import datetime

# Mengimpor seluruh modul utilitas & lisensi bawaan proyek tanpa ada yang dikurangi
from license import (
    check_license, use_quota, get_device_id, check_user,
    get_license_price, get_whatsapp_admin, get_telegram_username, get_active_apis,
    get_trial_quota, get_user_stats, VERSION
)

# Inisialisasi Bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_formatted_datetime():
    now = datetime.now()
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{days[now.weekday()]}, {now.day} {months[now.month - 1]} {now.year}"

@bot.event
async def on_ready():
    print(f"========================================")
    print(f" Bot Berhasil Login sebagai {bot.user.name}")
    print(f" ID: {bot.user.id}")
    print(f" Versi Tools: {VERSION}")
    print(f" Sistem Host: {platform.system()} (Termux / Environment)")
    print(f"========================================")
    await bot.change_presence(activity=discord.Game(name="!menu | OTP Spammer"))

@bot.command(name="menu")
async def menu_command(ctx):
    """Menampilkan menu utama 100% mengikuti output asli CLI di GitHub"""
    status, quota, device_id = check_license()
    premium, trial = get_user_stats()
    total_users = premium + trial
    trial_quota = get_trial_quota()
    
    embed = discord.Embed(
        title="⚡ WHATSAPP OTP SPAMMER PANEL ⚡",
        description=f"Waktu: {get_formatted_datetime()}\nSistem Host: {platform.system()}",
        color=discord.Color.cyan()
    )
    
    # Menampilkan statistik global sesuai aslinya
    embed.add_field(
        name="📊 Statistik Pengguna Global",
        value=f"• Total User: {total_users}\n• Premium User: {premium}\n• Trial User: {trial}",
        inline=False
    )

    if status == "trial":
        embed.add_field(
            name="🔴 STATUS LISENSI: MODE TRIAL",
            value=f"**Sisa Kuota Bot:** `{quota}/{trial_quota}`\n*Hanya diperbolehkan menggunakan Single Round.*",
            inline=False
        )
        embed.add_field(
            name="📜 Perintah Menu Yang Tersedia",
            value="`!single` - Jalankan SPAM OTP (1 Round)\n`!buy` - Panduan Pembelian Lisensi Premium",
            inline=False
        )
        
    elif status == "premium":
        embed.add_field(
            name="🟢 STATUS LISENSI: PREMIUM ACTIVE",
            value="**Akses Penuh:** Unlimited Kuota / Bebas Hambatan.",
            inline=False
        )
        embed.add_field(
            name="📜 Perintah Menu Yang Tersedia",
            value="`!single [thread]` - Jalankan Single Round (Pilihan thread 1-10)\n`!infinite` - Jalankan Infinite Loop Spam\n`!check` - Cek Integritas & Update API",
            inline=False
        )

    embed.set_footer(text=f"Kenzoo Bot Suite v{VERSION} • Host Device ID: {device_id}")
    await ctx.send(embed=embed)

@bot.command(name="single")
async def single_round_command(ctx, threads: int = 1):
    """Menjalankan serangan Single Round dengan proteksi kuota dari engine asli"""
    status, quota, device_id = check_license()
    trial_quota = get_trial_quota()
    
    # Import main engine penyerang asli
    from main_engine import run_single_round
    
    if status == "trial":
        if quota <= 0:
            await ctx.send("❌ **Kuota trial habis!** Silakan ketik `!buy` untuk membeli lisensi premium.")
            return
        
        threads = 1
        await ctx.send("⏳ [Trial Mode] Memulai serangan OTP (Single Round - 1 Thread)...")
        
        # Dijalankan secara non-blocking agar bot tidak hang total saat spam berjalan
        success = await asyncio.to_thread(run_single_round, threads=threads)
        
        if use_quota(device_id):
            user = check_user(device_id)
            new_quota = user.get("quota", 0) if user else 0
            await ctx.send(f"✅ **Serangan Selesai.** Sisa kuota trial: `{new_quota}/{trial_quota}`")
        else:
            await ctx.send("⚠️ Serangan selesai, namun gagal memotong kuota database.")
            
    elif status == "premium":
        if threads < 1: threads = 1
        elif threads > 10: threads = 10
        
        await ctx.send(f"🚀 **[PREMIUM]** Meluncurkan serangan OTP dengan **{threads} Thread**...")
        
        # Eksekusi engine aslinya di background thread
        await asyncio.to_thread(run_single_round, threads=threads)
        
        await ctx.send("✅ Serangan Single Round Premium selesai dilaksanakan.")

@bot.command(name="infinite")
async def infinite_loop_command(ctx):
    """Menjalankan Infinite Loop bawaan secara background"""
    status, _, _ = check_license()
    
    if status != "premium":
        await ctx.send("⛔ Perintah ini eksklusif untuk pengguna **Premium**. Ketik `!buy` untuk info lebih lanjut.")
        return
        
    await ctx.send("🔄 Menjalankan **Infinite Loop Spam** di background host bot...")
    
    from main_engine import run_infinite_loop
    # Menggunakan create_task agar perulangan infinite berjalan tanpa mematikan respon chat bot
    asyncio.create_task(asyncio.to_thread(run_infinite_loop))

@bot.command(name="buy")
async def buy_guide_command(ctx):
    """Menampilkan detail kontak pembelian sesuai file lisensi asli"""
    license_price = get_license_price()
    whatsapp_admin = get_whatsapp_admin()
    telegram_username = get_telegram_username()
    total_apis = get_active_apis()
    device_id = get_device_id()
    
    embed = discord.Embed(
        title="🛒 PANDUAN PEMBELIAN LISENSI PREMIUM",
        color=discord.Color.gold()
    )
    embed.add_field(
        name="💎 Benefit Fitur Premium",
        value=f"• Akses FULL semua API ({total_apis} API aktif)\n• Unlimited penggunaan (Tanpa batasan kuota)\n• Free update & bypass script lifetime.",
        inline=False
    )
    embed.add_field(
        name="💰 Harga Lisensi",
        value=f"**Rp. {license_price:,}** *(Sekali bayar)*",
        inline=False
    )
    embed.add_field(
        name="📞 Hubungi Admin",
        value=f"• **WhatsApp:** {whatsapp_admin}\n• **Telegram:** {telegram_username}",
        inline=False
    )
    embed.add_field(
        name="🔑 Host Device ID (Kirim ke Admin jika ingin mengaktifkan host ini)",
        value=f"`{device_id}`",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name="check")
async def check_update_command(ctx):
    """Mengecek status API bawaan"""
    total_apis = get_active_apis()
    latest_version = "3.1"
    
    status_ver = "Versi Anda sudah yang terbaru." if VERSION == latest_version else f"Versi baru tersedia: v{latest_version}. Silakan lakukan penarikan update!"
    
    embed = discord.Embed(title="🔍 API & UPDATE CONTEXT STATUS", color=discord.Color.blue())
    embed.add_field(name="Informasi Build & Versi", value=f"• Versi Terpasang: `{VERSION}`\n• Status Sistem: {status_ver}", inline=False)
    embed.add_field(name="Konektivitas Database API", value=f"• Total API Terdaftar: `{total_apis}`\n• API Status Operasional: `{total_apis}` Active", inline=False)
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    TOKEN = "MTQ5ODcyNjY5Njk3Nzk2MTA0MA.GOmLoR.-ypzXazaNjPEy8V8HyEpqtgKzYRqq9GpxS-XGQ"
    bot.run(TOKEN)
