/* CODE_BEGIN */
int call_probe(struct spi_driver *sdrv)
{
	return sdrv->probe(0);
}
/* CODE_END */
