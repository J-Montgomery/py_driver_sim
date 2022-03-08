/* CODE_BEGIN */
int spi_call_probe(struct spi_driver *sdrv, struct spi_device *spi)
{
	return sdrv->probe(spi);
}
/* CODE_END */
